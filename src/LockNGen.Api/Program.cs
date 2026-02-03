using LockNGen.Infrastructure.Data;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

// Database configuration
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");
if (string.IsNullOrEmpty(connectionString))
{
    // InMemory fallback for local dev without Docker
    builder.Services.AddDbContext<AppDbContext>(options =>
        options.UseInMemoryDatabase("LockNGen"));
}
else
{
    builder.Services.AddDbContext<AppDbContext>(options =>
        options.UseNpgsql(connectionString));
}

// Health checks
builder.Services.AddHealthChecks()
    .AddDbContextCheck<AppDbContext>();

var app = builder.Build();

// Ensure database is created
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    db.Database.EnsureCreated();
}

// Health endpoint
app.MapHealthChecks("/health");

// Root endpoint
app.MapGet("/", () => Results.Ok(new { 
    service = "LockN Gen", 
    version = "0.1.0",
    status = "running"
}));

app.Run();
