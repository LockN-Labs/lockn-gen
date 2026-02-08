# Build stage
FROM mcr.microsoft.com/dotnet/sdk:9.0.2 AS build
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
FROM mcr.microsoft.com/dotnet/aspnet:9.0.2 AS runtime

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

WORKDIR /app

# Install wget for health checks
RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

# Copy published app and set ownership
COPY --from=build /app/publish .
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

# Run the app
ENV ASPNETCORE_URLS=http://+:8080
ENTRYPOINT ["dotnet", "LockNGen.Api.dll"]
