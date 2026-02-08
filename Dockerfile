# Build stage
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /src

# Copy solution and project files
COPY LockNGen.sln .
COPY src/LockNGen.Domain/LockNGen.Domain.csproj src/LockNGen.Domain/
COPY src/LockNGen.Infrastructure/LockNGen.Infrastructure.csproj src/LockNGen.Infrastructure/
COPY src/LockNGen.Api/LockNGen.Api.csproj src/LockNGen.Api/

# Restore dependencies
RUN dotnet restore

# Copy all source code
COPY . .

# Build and publish
WORKDIR /src/src/LockNGen.Api
RUN dotnet publish -c Release -o /app/publish --no-restore

# Runtime stage
FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS runtime
WORKDIR /app

# Install wget for health checks
RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

# Copy published app
COPY --from=build /app/publish .

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

# Run the app
ENV ASPNETCORE_URLS=http://+:8080
RUN groupadd -r appuser && useradd -r -g appuser appuser && chown -R appuser:appuser /app
USER appuser

ENTRYPOINT ["dotnet", "LockNGen.Api.dll"]
