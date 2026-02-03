using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using LockNGen.Domain.Entities;

namespace LockNGen.Domain.Services
{
    public interface IApiKeyService
    {
        Task<(ApiKey key, string plainTextKey)> CreateKeyAsync(string name, bool isAdmin = false, int? rateLimit = null);
        Task<ApiKey?> ValidateKeyAsync(string plainTextKey);
        Task<IEnumerable<ApiKey>> GetAllKeysAsync();
        Task<bool> RevokeKeyAsync(Guid keyId);
        Task UpdateLastUsedAsync(Guid keyId);
        Task<KeyUsageStats?> GetKeyUsageAsync(Guid keyId);
    }

    public record KeyUsageStats(
        int TotalRequests,
        int RequestsToday,
        DateTime? LastUsedAt,
        int RemainingRequests
    );
}
