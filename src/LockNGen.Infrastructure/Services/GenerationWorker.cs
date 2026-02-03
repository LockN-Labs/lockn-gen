using LockNGen.Domain.Entities;
using LockNGen.Domain.Services;
using LockNGen.Infrastructure.ComfyUi;
using LockNGen.Infrastructure.Data;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using LockNGen.Domain.DTOs;

namespace LockNGen.Infrastructure.Services;

/// <summary>
/// Background worker that processes queued generations.
/// </summary>
public class GenerationWorker : BackgroundService
{
    private readonly IServiceScopeFactory _scopeFactory;
    private readonly IComfyUiClient _comfyUi;
    private readonly IWorkflowLoader _workflowLoader;
    private readonly ComfyUiOptions _options;
    private readonly ILogger<GenerationWorker> _logger;

    public GenerationWorker(
        IServiceScopeFactory scopeFactory,
        IComfyUiClient comfyUi,
        IWorkflowLoader workflowLoader,
        IOptions<ComfyUiOptions> options,
        ILogger<GenerationWorker> logger)
    {
        _scopeFactory = scopeFactory;
        _comfyUi = comfyUi;
        _workflowLoader = workflowLoader;
        _options = options.Value;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        _logger.LogInformation("GenerationWorker starting");

        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                await ProcessNextGeneration(stoppingToken);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing generation");
            }

            await Task.Delay(5000, stoppingToken); // Poll every 5 seconds
        }
    }

    private async Task ProcessNextGeneration(CancellationToken ct)
    {
        using var scope = _scopeFactory.CreateScope();
        var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();

        // Get next queued generation
        var generation = await db.Generations
            .Where(g => g.Status == GenerationStatus.Queued)
            .OrderBy(g => g.CreatedAt)
            .FirstOrDefaultAsync(ct);

        if (generation == null)
            return;

        _logger.LogInformation("Processing generation {Id}", generation.Id);

        try
        {
            // Mark as processing
            generation.Status = GenerationStatus.Processing;
            generation.UpdatedAt = DateTime.UtcNow;
            await db.SaveChangesAsync(ct);

            // Load workflow template
            var templateName = $"txt2img-{generation.Model}";
            var parameters = new GenerationParameters
            {
                Prompt = generation.Prompt,
                NegativePrompt = generation.NegativePrompt,
                Steps = generation.Steps,
                Guidance = generation.Guidance,
                Seed = generation.Seed,
                Width = generation.Width,
                Height = generation.Height,
                Model = generation.Model
            };

            var workflow = await _workflowLoader.LoadAsync(templateName, parameters, ct);

            // Submit to ComfyUI
            var promptId = await _comfyUi.QueuePromptAsync(workflow, ct);
            generation.PromptId = promptId;
            await db.SaveChangesAsync(ct);

            // Poll for completion
            var timeout = DateTime.UtcNow.AddSeconds(_options.TimeoutSeconds);
            PromptHistory? history = null;

            while (DateTime.UtcNow < timeout && !ct.IsCancellationRequested)
            {
                await Task.Delay(_options.PollIntervalMs, ct);
                history = await _comfyUi.GetHistoryAsync(promptId, ct);

                if (history?.Status?.Completed == true)
                    break;
            }

            if (history?.Status?.Completed != true)
            {
                throw new TimeoutException($"Generation timed out after {_options.TimeoutSeconds}s");
            }

            // Find output image
            var imageOutput = history.Outputs?.Values
                .SelectMany(o => o.Images ?? [])
                .FirstOrDefault();

            if (imageOutput == null)
            {
                throw new InvalidOperationException("No output image found");
            }

            // Download and save image
            Directory.CreateDirectory(_options.OutputPath);
            var outputPath = Path.Combine(_options.OutputPath, $"{generation.Id}.png");

            await using var imageStream = await _comfyUi.GetImageAsync(
                imageOutput.Filename, imageOutput.Subfolder, imageOutput.Type, ct);
            await using var fileStream = File.Create(outputPath);
            await imageStream.CopyToAsync(fileStream, ct);

            // Update generation
            generation.Status = GenerationStatus.Completed;
            generation.OutputPath = outputPath;
            generation.CompletedAt = DateTime.UtcNow;
            generation.DurationMs = (int)(generation.CompletedAt.Value - generation.CreatedAt).TotalMilliseconds;
            generation.UpdatedAt = DateTime.UtcNow;

            _logger.LogInformation("Completed generation {Id} in {Duration}ms", generation.Id, generation.DurationMs);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed generation {Id}", generation.Id);
            generation.Status = GenerationStatus.Failed;
            generation.ErrorMessage = ex.Message;
            generation.UpdatedAt = DateTime.UtcNow;
        }

        await db.SaveChangesAsync(ct);
    }
}
