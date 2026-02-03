using LockNGen.Domain.DTOs;
using LockNGen.Domain.Entities;
using LockNGen.Domain.Services;
using LockNGen.Infrastructure.ComfyUi;
using LockNGen.Infrastructure.Data;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;

namespace LockNGen.Infrastructure.Services;

/// <summary>
/// Manages the generation queue.
/// </summary>
public class GenerationService : IGenerationService
{
    private readonly AppDbContext _db;
    private readonly ComfyUiOptions _options;
    private readonly ILogger<GenerationService> _logger;

    public GenerationService(AppDbContext db, IOptions<ComfyUiOptions> options, ILogger<GenerationService> logger)
    {
        _db = db;
        _options = options.Value;
        _logger = logger;
    }

    public async Task<Generation> QueueAsync(GenerationParameters request, CancellationToken ct = default)
    {
        var generation = new Generation
        {
            Id = Guid.NewGuid(),
            Name = request.Prompt.Length > 50 ? request.Prompt[..50] + "..." : request.Prompt,
            Prompt = request.Prompt,
            NegativePrompt = request.NegativePrompt,
            Model = request.Model,
            Steps = request.Steps,
            Guidance = request.Guidance,
            Seed = request.Seed,
            Width = request.Width,
            Height = request.Height,
            Status = GenerationStatus.Queued,
            CreatedAt = DateTime.UtcNow
        };

        _db.Generations.Add(generation);
        await _db.SaveChangesAsync(ct);

        _logger.LogInformation("Queued generation {Id}: {Prompt}", generation.Id, generation.Name);
        return generation;
    }

    public async Task<Generation?> GetAsync(Guid id, CancellationToken ct = default)
    {
        return await _db.Generations.FindAsync([id], ct);
    }

    public async Task<IReadOnlyList<Generation>> ListAsync(int skip = 0, int take = 20, CancellationToken ct = default)
    {
        return await _db.Generations
            .OrderByDescending(g => g.CreatedAt)
            .Skip(skip)
            .Take(take)
            .ToListAsync(ct);
    }

    public async Task<bool> CancelAsync(Guid id, CancellationToken ct = default)
    {
        var generation = await _db.Generations.FindAsync([id], ct);
        if (generation == null || generation.Status != GenerationStatus.Queued)
            return false;

        generation.Status = GenerationStatus.Cancelled;
        generation.UpdatedAt = DateTime.UtcNow;
        await _db.SaveChangesAsync(ct);

        _logger.LogInformation("Cancelled generation {Id}", id);
        return true;
    }

    public Task<Stream?> GetImageStreamAsync(Guid id, CancellationToken ct = default)
    {
        var path = Path.Combine(_options.OutputPath, $"{id}.png");
        if (!File.Exists(path))
            return Task.FromResult<Stream?>(null);

        return Task.FromResult<Stream?>(File.OpenRead(path));
    }
}
