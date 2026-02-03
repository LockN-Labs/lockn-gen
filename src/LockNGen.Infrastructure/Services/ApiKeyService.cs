using System;
using System.Collections.Generic;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;
using LockNGen.Domain.Entities;
using LockNGen.Domain.Services;
using LockNGen.Infrastructure.Data;
using Microsoft.EntityFrameworkCore;

namespace LockNGen.Infrastructure.Services;

public class ApiKeyService(AppDbContext context) : IApiKeyService
{
    public async Task<(ApiKey key, string plainTextKey)> CreateKeyAsync(string name, bool isAdmin = false, int? rateLimit = null)
    {
        var keyBytes = new byte[32];
        using var rng = RandomNumberGenerator.Create();
        rng.GetBytes(keyBytes);

        var base64Key = Convert.ToBase64String(keyBytes)
            .Replace('+', '-')
            .Replace('/', '_')
            .TrimEnd('=');

        var prefix = "lg_live_";
        var fullKey = prefix + base64Key;
        var keyHash = ComputeSha256Hash(fullKey);

        var keyPrefix = base64Key.Substring(0, Math.Min(8, base64Key.Length));

        var apiKey = new ApiKey
        {
            Name = name,
            KeyHash = keyHash,
            KeyPrefix = keyPrefix,
            IsAdmin = isAdmin,
            RateLimit = rateLimit ?? 100
        };

        context.ApiKeys.Add(apiKey);
        await context.SaveChangesAsync();

        return (apiKey, fullKey);
    }

    public async Task<ApiKey?> ValidateKeyAsync(string plainTextKey)
    {
        var keyHash = ComputeSha256Hash(plainTextKey);
        var apiKey = await context.ApiKeys.FirstOrDefaultAsync(k => k.KeyHash == keyHash);

        if (apiKey == null || !apiKey.IsValid)
            return null;

        _ = Task.Run(() => UpdateLastUsedAsync(apiKey.Id));

        return apiKey;
    }

    public async Task<IEnumerable<ApiKey>> GetAllKeysAsync()
    {
        return await context.ApiKeys.Where(k => k.RevokedAt == null).ToListAsync();
    }

    public async Task<bool> RevokeKeyAsync(Guid keyId)
    {
        var apiKey = await context.ApiKeys.FindAsync(keyId);
        if (apiKey == null)
            return false;

        apiKey.RevokedAt = DateTime.UtcNow;
        await context.SaveChangesAsync();
        return true;
    }

    public async Task UpdateLastUsedAsync(Guid keyId)
    {
        var apiKey = await context.ApiKeys.FindAsync(keyId);
        if (apiKey == null)
            return;

        if (apiKey.LastUsedAt == null || apiKey.LastUsedAt < DateTime.UtcNow.AddMinutes(-1))
        {
            apiKey.LastUsedAt = DateTime.UtcNow;
            await context.SaveChangesAsync();
        }
    }

    public async Task<KeyUsageStats?> GetKeyUsageAsync(Guid keyId)
    {
        var apiKey = await context.ApiKeys.FindAsync(keyId);
        if (apiKey == null)
            return null;

        return new KeyUsageStats(
            TotalRequests: 0,
            RequestsToday: 0,
            LastUsedAt: apiKey.LastUsedAt,
            RemainingRequests: apiKey.RateLimit
        );
    }

    private static string ComputeSha256Hash(string input)
    {
        using var sha256 = SHA256.Create();
        var bytes = sha256.ComputeHash(Encoding.UTF8.GetBytes(input));
        var builder = new StringBuilder();
        foreach (var b in bytes)
            builder.Append(b.ToString("x2"));
        return builder.ToString();
    }
}
