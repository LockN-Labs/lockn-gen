using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace LockNGen.Domain.Services
{
    public interface IMetricsService
    {
        Task<AdminStatsDto> GetStatsAsync();
        Task<List<ApiKeyUsageDto>> GetApiKeyUsageAsync(int hours = 24);
        Task<int> GetQueueDepthAsync();
    }

    public record AdminStatsDto(
        int TotalGenerations,
        int SuccessCount,
        int FailedCount,
        int InProgressCount,
        double SuccessRate
    );

    public record ApiKeyUsageDto(
        Guid ApiKeyId,
        string KeyName,
        int RequestCount,
        DateTime LastUsed
    );
}
