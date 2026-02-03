using LockNGen.Domain.Entities;
using LockNGen.Domain.Services;
using LockNGen.Infrastructure.Data;
using Microsoft.EntityFrameworkCore;

namespace LockNGen.Infrastructure.Services;

public class MetricsService : IMetricsService
{
    private readonly AppDbContext _context;

    public MetricsService(AppDbContext context)
    {
        _context = context;
    }

    public async Task<AdminStatsDto> GetStatsAsync()
    {
        var stats = await _context.Generations
            .GroupBy(g => g.Status)
            .Select(g => new { Status = g.Key, Count = g.Count() })
            .ToListAsync();

        var total = stats.Sum(s => s.Count);
        var successCount = stats.FirstOrDefault(s => s.Status == GenerationStatus.Completed)?.Count ?? 0;
        var failedCount = stats.FirstOrDefault(s => s.Status == GenerationStatus.Failed)?.Count ?? 0;
        var inProgressCount = stats
            .Where(s => s.Status == GenerationStatus.Queued || s.Status == GenerationStatus.Processing)
            .Sum(s => s.Count);
        
        var successRate = total > 0 ? (double)successCount / total * 100 : 0;

        return new AdminStatsDto(
            TotalGenerations: total,
            SuccessCount: successCount,
            FailedCount: failedCount,
            InProgressCount: inProgressCount,
            SuccessRate: Math.Round(successRate, 2)
        );
    }

    public async Task<List<ApiKeyUsageDto>> GetApiKeyUsageAsync(int hours = 24)
    {
        var fromDate = DateTime.UtcNow.AddHours(-hours);
        
        var apiKeys = await _context.ApiKeys
            .Select(k => new ApiKeyUsageDto(
                ApiKeyId: k.Id,
                KeyName: k.Name,
                RequestCount: 0, // TODO: Add tracking once Generation has ApiKeyId
                LastUsed: k.LastUsedAt ?? k.CreatedAt
            ))
            .ToListAsync();

        return apiKeys;
    }

    public async Task<int> GetQueueDepthAsync()
    {
        return await _context.Generations
            .CountAsync(g => g.Status == GenerationStatus.Queued || g.Status == GenerationStatus.Processing);
    }
}
