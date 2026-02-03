using LockNGen.Domain.Entities;
using Microsoft.EntityFrameworkCore;

namespace LockNGen.Infrastructure.Data;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
    {
    }

    public DbSet<Generation> Generations => Set<Generation>();
    public DbSet<ApiKey> ApiKeys => Set<ApiKey>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        modelBuilder.Entity<Generation>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Name).HasMaxLength(255);
            entity.Property(e => e.Prompt).IsRequired().HasMaxLength(4000);
            entity.Property(e => e.NegativePrompt).HasMaxLength(4000);
            entity.Property(e => e.Model).IsRequired().HasMaxLength(100);
            entity.Property(e => e.PromptId).HasMaxLength(100);
            entity.Property(e => e.OutputPath).HasMaxLength(500);
            entity.Property(e => e.ThumbnailPath).HasMaxLength(500);
            entity.Property(e => e.ErrorMessage).HasMaxLength(2000);
            entity.HasIndex(e => e.Status);
            entity.HasIndex(e => e.CreatedAt);
        });

        modelBuilder.Entity<ApiKey>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Name).IsRequired().HasMaxLength(255);
            entity.Property(e => e.KeyHash).IsRequired().HasMaxLength(64);
            entity.Property(e => e.KeyPrefix).IsRequired().HasMaxLength(16);
            entity.HasIndex(e => e.KeyHash).IsUnique();
            entity.HasIndex(e => e.KeyPrefix);
        });
    }
}
