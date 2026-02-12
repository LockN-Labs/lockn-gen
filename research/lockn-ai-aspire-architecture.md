# LockN AI — .NET Aspire Architecture Design Document

> **Version:** 1.0  
> **Date:** 2026-02-11  
> **Author:** LockN Labs Architecture Team  
> **Status:** Draft — Pending CEO Review

---

## Table of Contents

1. [Aspire Solution Structure](#1-aspire-solution-structure)
2. [Provider Abstraction Interfaces](#2-provider-abstraction-interfaces)
3. [Service Discovery & Communication](#3-service-discovery--communication)
4. [Dependency Injection & Provider Registration](#4-dependency-injection--provider-registration)
5. [OpenTelemetry Integration](#5-opentelemetry-integration)
6. [Deployment Topology](#6-deployment-topology)
7. [NuGet Packaging Strategy](#7-nuget-packaging-strategy)

---

## 1. Aspire Solution Structure

### 1.1 Repository Layout

```
lockn-ai/
├── LockN.sln
│
├── src/
│   ├── AppHost/
│   │   └── LockN.AppHost/                    # Aspire orchestrator
│   │       ├── LockN.AppHost.csproj
│   │       └── Program.cs
│   │
│   ├── ServiceDefaults/
│   │   └── LockN.ServiceDefaults/            # Shared Aspire defaults (OTel, health, resilience)
│   │       ├── LockN.ServiceDefaults.csproj
│   │       └── Extensions.cs
│   │
│   ├── Abstractions/
│   │   └── LockN.Abstractions/               # All provider interfaces + DTOs
│   │       ├── LockN.Abstractions.csproj
│   │       ├── Chat/
│   │       │   ├── ILocknChat.cs
│   │       │   ├── Models/
│   │       │   └── Events/
│   │       ├── Auth/
│   │       ├── Work/
│   │       ├── Doc/
│   │       ├── Mem/
│   │       ├── Arch/
│   │       ├── Flow/
│   │       ├── Watch/
│   │       ├── Voice/
│   │       └── Common/
│   │           ├── ILocknModule.cs            # Base module lifecycle interface
│   │           ├── LocknResult.cs             # Standard result wrapper
│   │           ├── PagedResult.cs
│   │           └── LocknEvent.cs              # Base event type
│   │
│   ├── Providers/                             # Concrete implementations
│   │   ├── LockN.Chat.Matrix/
│   │   ├── LockN.Chat.Slack/
│   │   ├── LockN.Auth.Zitadel/
│   │   ├── LockN.Auth.Auth0/
│   │   ├── LockN.Work.Linear/
│   │   ├── LockN.Work.Plane/
│   │   ├── LockN.Doc.Notion/
│   │   ├── LockN.Doc.AFFiNE/
│   │   ├── LockN.Mem.Qdrant/
│   │   ├── LockN.Arch.D2/
│   │   ├── LockN.Arch.Mermaid/
│   │   ├── LockN.Flow.Temporal/
│   │   ├── LockN.Watch.OpenTelemetry/
│   │   ├── LockN.Voice.FishSpeech/
│   │   └── LockN.Voice.ElevenLabs/
│   │
│   ├── Services/                              # Aspire service projects (API hosts)
│   │   ├── LockN.Chat.Service/               # gRPC + REST API for Chat
│   │   ├── LockN.Auth.Service/
│   │   ├── LockN.Work.Service/
│   │   ├── LockN.Doc.Service/
│   │   ├── LockN.Mem.Service/
│   │   ├── LockN.Flow.Service/
│   │   ├── LockN.Voice.Service/
│   │   └── LockN.Gateway/                    # Edge API gateway / BFF
│   │
│   ├── Hosting/                               # Custom Aspire hosting integrations
│   │   ├── LockN.Hosting.Temporal/           # builder.AddTemporal()
│   │   ├── LockN.Hosting.Dendrite/           # builder.AddDendrite()
│   │   └── LockN.Hosting.D2/                 # builder.AddD2()
│   │
│   └── Legacy/                                # Migrated existing services
│       ├── LockN.Swap/                        # lockn-swap → Aspire project
│       ├── LockN.ApiKeys/
│       ├── LockN.Logger/
│       └── LockN.Listen/
│
├── containers/
│   └── openclaw/                              # OpenClaw Node.js runtime
│       ├── Dockerfile
│       └── ...
│
├── tests/
│   ├── LockN.Abstractions.Tests/
│   ├── LockN.Chat.Matrix.Tests/
│   └── ...
│
└── docs/
    └── architecture/
```

### 1.2 AppHost — `Program.cs`

```csharp
using LockN.AppHost;

var builder = DistributedApplication.CreateBuilder(args);

// ── Infrastructure Resources ────────────────────────────────────────

var qdrant = builder.AddQdrant("qdrant")
    .WithDataVolume("lockn-qdrant-data")
    .WithLifetime(ContainerLifetime.Persistent);

var temporal = builder.AddContainer("temporal", "temporalio/auto-setup", "latest")
    .WithEndpoint(port: 7233, targetPort: 7233, name: "grpc", scheme: "http")
    .WithEndpoint(port: 8233, targetPort: 8233, name: "ui", scheme: "http")
    .WithLifetime(ContainerLifetime.Persistent);

var dendrite = builder.AddContainer("dendrite", "matrixdotorg/dendrite-monolith", "latest")
    .WithEndpoint(port: 8008, targetPort: 8008, name: "http", scheme: "http")
    .WithBindMount("./config/dendrite", "/etc/dendrite")
    .WithDataVolume("lockn-dendrite-data")
    .WithLifetime(ContainerLifetime.Persistent);

var grafana = builder.AddContainer("grafana", "grafana/grafana", "latest")
    .WithEndpoint(port: 3000, targetPort: 3000, name: "http", scheme: "http")
    .WithDataVolume("lockn-grafana-data")
    .WithLifetime(ContainerLifetime.Persistent);

var redis = builder.AddRedis("redis")
    .WithDataVolume("lockn-redis-data")
    .WithLifetime(ContainerLifetime.Persistent);

// ── OpenClaw (Node.js Runtime) ──────────────────────────────────────

var openclaw = builder.AddDockerfile("openclaw", "./containers/openclaw")
    .WithHttpEndpoint(port: 3100, targetPort: 3100, name: "api")
    .WithEnvironment("LOCKN_GATEWAY_URL", "")    // Populated by reference
    .WithReference(redis)
    .WithReference(qdrant);

// ── .NET Service Projects ───────────────────────────────────────────

var gateway = builder.AddProject<Projects.LockN_Gateway>("gateway")
    .WithReference(redis)
    .WithExternalHttpEndpoints();

var chatService = builder.AddProject<Projects.LockN_Chat_Service>("chat-service")
    .WithReference(dendrite)
    .WithReference(redis)
    .WithReference(gateway);

var authService = builder.AddProject<Projects.LockN_Auth_Service>("auth-service")
    .WithReference(redis)
    .WithReference(gateway);

var workService = builder.AddProject<Projects.LockN_Work_Service>("work-service")
    .WithReference(gateway);

var docService = builder.AddProject<Projects.LockN_Doc_Service>("doc-service")
    .WithReference(gateway);

var memService = builder.AddProject<Projects.LockN_Mem_Service>("mem-service")
    .WithReference(qdrant)
    .WithReference(gateway);

var flowService = builder.AddProject<Projects.LockN_Flow_Service>("flow-service")
    .WithReference(temporal)
    .WithReference(gateway);

var voiceService = builder.AddProject<Projects.LockN_Voice_Service>("voice-service")
    .WithReference(gateway);

// ── Wire OpenClaw to all services ───────────────────────────────────

openclaw
    .WithReference(gateway)
    .WithReference(chatService)
    .WithReference(memService);

// ── Legacy services (migrated) ──────────────────────────────────────

var swap = builder.AddProject<Projects.LockN_Swap>("lockn-swap")
    .WithReference(redis);

var apikeys = builder.AddProject<Projects.LockN_ApiKeys>("lockn-apikeys")
    .WithReference(redis);

builder.Build().Run();
```

### 1.3 ServiceDefaults — `Extensions.cs`

```csharp
namespace LockN.ServiceDefaults;

public static class Extensions
{
    public static IHostApplicationBuilder AddServiceDefaults(
        this IHostApplicationBuilder builder)
    {
        builder.ConfigureOpenTelemetry();
        builder.AddDefaultHealthChecks();
        builder.Services.AddServiceDiscovery();

        builder.Services.ConfigureHttpClientDefaults(http =>
        {
            http.AddStandardResilienceHandler();
            http.AddServiceDiscovery();
        });

        return builder;
    }

    public static IHostApplicationBuilder ConfigureOpenTelemetry(
        this IHostApplicationBuilder builder)
    {
        builder.Logging.AddOpenTelemetry(logging =>
        {
            logging.IncludeFormattedMessage = true;
            logging.IncludeScopes = true;
        });

        builder.Services.AddOpenTelemetry()
            .WithMetrics(metrics =>
            {
                metrics
                    .AddAspNetCoreInstrumentation()
                    .AddHttpClientInstrumentation()
                    .AddRuntimeInstrumentation()
                    // LockN custom meters
                    .AddMeter("LockN.Chat")
                    .AddMeter("LockN.Auth")
                    .AddMeter("LockN.Work")
                    .AddMeter("LockN.Mem")
                    .AddMeter("LockN.Flow")
                    .AddMeter("LockN.Voice");
            })
            .WithTracing(tracing =>
            {
                tracing
                    .AddAspNetCoreInstrumentation()
                    .AddGrpcClientInstrumentation()
                    .AddHttpClientInstrumentation()
                    .AddSource("LockN.*");
            });

        builder.AddOpenTelemetryExporters();
        return builder;
    }

    private static IHostApplicationBuilder AddOpenTelemetryExporters(
        this IHostApplicationBuilder builder)
    {
        var useOtlpExporter = !string.IsNullOrWhiteSpace(
            builder.Configuration["OTEL_EXPORTER_OTLP_ENDPOINT"]);

        if (useOtlpExporter)
        {
            builder.Services.AddOpenTelemetry()
                .UseOtlpExporter();
        }

        return builder;
    }

    public static IHostApplicationBuilder AddDefaultHealthChecks(
        this IHostApplicationBuilder builder)
    {
        builder.Services.AddHealthChecks()
            .AddCheck("self", () => HealthCheckResult.Healthy(), ["live"]);

        return builder;
    }

    public static WebApplication MapDefaultEndpoints(this WebApplication app)
    {
        app.MapHealthChecks("/health");
        app.MapHealthChecks("/alive", new()
        {
            Predicate = r => r.Tags.Contains("live")
        });
        return app;
    }
}
```

---

## 2. Provider Abstraction Interfaces

### 2.1 Common Base Types

```csharp
// ── LockN.Abstractions/Common/ ──────────────────────────────────────

namespace LockN.Abstractions.Common;

/// <summary>
/// Base lifecycle interface for all LockN modules.
/// </summary>
public interface ILocknModule
{
    /// <summary>Unique module identifier (e.g., "chat.matrix").</summary>
    string ProviderId { get; }

    /// <summary>Initialize the provider (connect, authenticate, etc.).</summary>
    Task InitializeAsync(CancellationToken ct = default);

    /// <summary>Check if the provider is healthy and connected.</summary>
    Task<HealthStatus> CheckHealthAsync(CancellationToken ct = default);

    /// <summary>Gracefully shut down the provider.</summary>
    Task ShutdownAsync(CancellationToken ct = default);
}

/// <summary>Standard result wrapper for all operations.</summary>
public record LocknResult<T>
{
    public bool Success { get; init; }
    public T? Data { get; init; }
    public LocknError? Error { get; init; }
    public Dictionary<string, string> Metadata { get; init; } = [];

    public static LocknResult<T> Ok(T data) => new() { Success = true, Data = data };
    public static LocknResult<T> Fail(string code, string message) =>
        new() { Success = false, Error = new(code, message) };
}

public record LocknError(string Code, string Message, Exception? Inner = null);

/// <summary>Paginated result set.</summary>
public record PagedResult<T>
{
    public required IReadOnlyList<T> Items { get; init; }
    public required int TotalCount { get; init; }
    public string? Cursor { get; init; }
    public bool HasMore { get; init; }
}

/// <summary>Base event type for all module events.</summary>
public record LocknEvent
{
    public required string EventType { get; init; }
    public required string SourceModule { get; init; }
    public required DateTimeOffset Timestamp { get; init; }
    public string? CorrelationId { get; init; }
    public Dictionary<string, object> Properties { get; init; } = [];
}

/// <summary>Typed event with payload.</summary>
public record LocknEvent<T> : LocknEvent
{
    public required T Payload { get; init; }
}
```

### 2.2 ILocknChat — Messaging & Communications

```csharp
namespace LockN.Abstractions.Chat;

// ── Models ──────────────────────────────────────────────────────────

public record ChatChannel
{
    public required string Id { get; init; }
    public required string Name { get; init; }
    public string? Topic { get; init; }
    public string? Purpose { get; init; }
    public bool IsPrivate { get; init; }
    public bool IsArchived { get; init; }
    public DateTimeOffset CreatedAt { get; init; }
    public IReadOnlyList<string> MemberIds { get; init; } = [];
}

public record ChatMessage
{
    public required string Id { get; init; }
    public required string ChannelId { get; init; }
    public required string SenderId { get; init; }
    public required string Content { get; init; }
    public string? ThreadId { get; init; }
    public string? ReplyToId { get; init; }
    public DateTimeOffset Timestamp { get; init; }
    public DateTimeOffset? EditedAt { get; init; }
    public IReadOnlyList<ChatAttachment> Attachments { get; init; } = [];
    public IReadOnlyList<ChatReaction> Reactions { get; init; } = [];
    public Dictionary<string, object> ProviderMetadata { get; init; } = [];
}

public record ChatAttachment
{
    public required string Id { get; init; }
    public required string FileName { get; init; }
    public required string ContentType { get; init; }
    public required long SizeBytes { get; init; }
    public required string Url { get; init; }
}

public record ChatReaction(string Emoji, string UserId, DateTimeOffset Timestamp);

public record ChatThread
{
    public required string Id { get; init; }
    public required string ChannelId { get; init; }
    public required string RootMessageId { get; init; }
    public int ReplyCount { get; init; }
    public DateTimeOffset LastReplyAt { get; init; }
    public IReadOnlyList<string> ParticipantIds { get; init; } = [];
}

public record ChatUser
{
    public required string Id { get; init; }
    public required string DisplayName { get; init; }
    public string? AvatarUrl { get; init; }
    public PresenceStatus Presence { get; init; }
    public string? StatusText { get; init; }
}

public enum PresenceStatus { Unknown, Online, Away, DoNotDisturb, Offline }

public record SendMessageRequest
{
    public required string ChannelId { get; init; }
    public required string Content { get; init; }
    public string? ThreadId { get; init; }
    public string? ReplyToId { get; init; }
    public IReadOnlyList<ChatAttachment>? Attachments { get; init; }
}

public record CreateChannelRequest
{
    public required string Name { get; init; }
    public string? Topic { get; init; }
    public bool IsPrivate { get; init; }
    public IReadOnlyList<string>? InviteUserIds { get; init; }
}

// ── Events ──────────────────────────────────────────────────────────

public record MessageReceivedEvent : LocknEvent<ChatMessage>;
public record MessageEditedEvent : LocknEvent<ChatMessage>;
public record MessageDeletedEvent : LocknEvent<string>;          // message ID
public record ReactionAddedEvent : LocknEvent<(string MessageId, ChatReaction Reaction)>;
public record PresenceChangedEvent : LocknEvent<(string UserId, PresenceStatus Status)>;
public record ChannelCreatedEvent : LocknEvent<ChatChannel>;
public record TypingEvent : LocknEvent<(string ChannelId, string UserId)>;

// ── Configuration ───────────────────────────────────────────────────

public class LocknChatOptions
{
    public const string SectionName = "LockN:Chat";
    public required string Provider { get; set; }            // "matrix" | "slack"
    public string? HomeserverUrl { get; set; }               // Matrix
    public string? AccessToken { get; set; }
    public string? BotUserId { get; set; }
    public string? SlackBotToken { get; set; }               // Slack
    public string? SlackAppToken { get; set; }
    public int MaxRetries { get; set; } = 3;
    public TimeSpan SyncTimeout { get; set; } = TimeSpan.FromSeconds(30);
}

// ── Interface ───────────────────────────────────────────────────────

/// <summary>
/// LockN Chat provider — unified messaging interface across Matrix, Slack, etc.
/// </summary>
public interface ILocknChat : ILocknModule
{
    // ── Channels ────────────────────────────────────────────────────

    /// <summary>List channels the bot has access to.</summary>
    Task<PagedResult<ChatChannel>> ListChannelsAsync(
        int limit = 50, string? cursor = null, CancellationToken ct = default);

    /// <summary>Get a specific channel by ID.</summary>
    Task<LocknResult<ChatChannel>> GetChannelAsync(
        string channelId, CancellationToken ct = default);

    /// <summary>Create a new channel.</summary>
    Task<LocknResult<ChatChannel>> CreateChannelAsync(
        CreateChannelRequest request, CancellationToken ct = default);

    /// <summary>Archive/delete a channel.</summary>
    Task<LocknResult<bool>> ArchiveChannelAsync(
        string channelId, CancellationToken ct = default);

    // ── Messages ────────────────────────────────────────────────────

    /// <summary>Send a message to a channel or thread.</summary>
    Task<LocknResult<ChatMessage>> SendMessageAsync(
        SendMessageRequest request, CancellationToken ct = default);

    /// <summary>Edit an existing message.</summary>
    Task<LocknResult<ChatMessage>> EditMessageAsync(
        string messageId, string newContent, CancellationToken ct = default);

    /// <summary>Delete a message.</summary>
    Task<LocknResult<bool>> DeleteMessageAsync(
        string messageId, CancellationToken ct = default);

    /// <summary>Fetch message history for a channel.</summary>
    Task<PagedResult<ChatMessage>> GetMessagesAsync(
        string channelId, int limit = 50, string? cursor = null,
        CancellationToken ct = default);

    // ── Threads ─────────────────────────────────────────────────────

    /// <summary>Get thread info and replies.</summary>
    Task<LocknResult<ChatThread>> GetThreadAsync(
        string threadId, CancellationToken ct = default);

    /// <summary>Reply to a thread.</summary>
    Task<LocknResult<ChatMessage>> ReplyToThreadAsync(
        string threadId, string content, CancellationToken ct = default);

    // ── Reactions ───────────────────────────────────────────────────

    /// <summary>Add a reaction to a message.</summary>
    Task<LocknResult<bool>> AddReactionAsync(
        string messageId, string emoji, CancellationToken ct = default);

    /// <summary>Remove a reaction from a message.</summary>
    Task<LocknResult<bool>> RemoveReactionAsync(
        string messageId, string emoji, CancellationToken ct = default);

    // ── Presence & Users ────────────────────────────────────────────

    /// <summary>Get user info including presence.</summary>
    Task<LocknResult<ChatUser>> GetUserAsync(
        string userId, CancellationToken ct = default);

    /// <summary>Set the bot's presence status.</summary>
    Task<LocknResult<bool>> SetPresenceAsync(
        PresenceStatus status, string? statusText = null,
        CancellationToken ct = default);

    // ── Events (Reactive) ───────────────────────────────────────────

    /// <summary>Observable stream of incoming messages.</summary>
    IObservable<MessageReceivedEvent> OnMessageReceived { get; }

    /// <summary>Observable stream of message edits.</summary>
    IObservable<MessageEditedEvent> OnMessageEdited { get; }

    /// <summary>Observable stream of reaction events.</summary>
    IObservable<ReactionAddedEvent> OnReactionAdded { get; }

    /// <summary>Observable stream of presence changes.</summary>
    IObservable<PresenceChangedEvent> OnPresenceChanged { get; }

    /// <summary>Observable stream of typing indicators.</summary>
    IObservable<TypingEvent> OnTyping { get; }
}
```

### 2.3 ILocknAuth — Identity & Authorization

```csharp
namespace LockN.Abstractions.Auth;

// ── Models ──────────────────────────────────────────────────────────

public record LocknIdentity
{
    public required string Id { get; init; }
    public required string Subject { get; init; }          // sub claim
    public required IdentityKind Kind { get; init; }       // Human, Agent, Service
    public required string DisplayName { get; init; }
    public string? Email { get; init; }
    public string? TenantId { get; init; }
    public IReadOnlyList<string> Roles { get; init; } = [];
    public IReadOnlyList<string> Permissions { get; init; } = [];
    public Dictionary<string, string> Claims { get; init; } = [];
}

public enum IdentityKind { Human, Agent, Service }

public record AuthToken
{
    public required string AccessToken { get; init; }
    public string? RefreshToken { get; init; }
    public required DateTimeOffset ExpiresAt { get; init; }
    public required string TokenType { get; init; }
    public IReadOnlyList<string> Scopes { get; init; } = [];
}

public record Tenant
{
    public required string Id { get; init; }
    public required string Name { get; init; }
    public string? Domain { get; init; }
    public TenantPlan Plan { get; init; }
    public Dictionary<string, string> Settings { get; init; } = [];
}

public enum TenantPlan { Free, Pro, Enterprise }

public record DelegationGrant
{
    public required string GrantId { get; init; }
    public required string GrantorId { get; init; }
    public required string DelegateId { get; init; }
    public required IReadOnlyList<string> Scopes { get; init; }
    public required DateTimeOffset ExpiresAt { get; init; }
}

public record AuthenticateRequest
{
    public required string GrantType { get; init; }       // "client_credentials", "authorization_code", "agent_token"
    public string? ClientId { get; init; }
    public string? ClientSecret { get; init; }
    public string? Code { get; init; }
    public string? RedirectUri { get; init; }
    public IReadOnlyList<string>? Scopes { get; init; }
}

// ── Events ──────────────────────────────────────────────────────────

public record AuthenticationSucceededEvent : LocknEvent<LocknIdentity>;
public record AuthenticationFailedEvent : LocknEvent<(string Subject, string Reason)>;
public record TokenRefreshedEvent : LocknEvent<(string Subject, DateTimeOffset NewExpiry)>;
public record PermissionDeniedEvent : LocknEvent<(string Subject, string Resource, string Action)>;

// ── Configuration ───────────────────────────────────────────────────

public class LocknAuthOptions
{
    public const string SectionName = "LockN:Auth";
    public required string Provider { get; set; }           // "zitadel" | "auth0"
    public required string Authority { get; set; }          // issuer URL
    public required string Audience { get; set; }
    public string? ClientId { get; set; }
    public string? ClientSecret { get; set; }
    public bool EnableAgentIdentity { get; set; } = true;
    public TimeSpan TokenCacheDuration { get; set; } = TimeSpan.FromMinutes(5);
}

// ── Interface ───────────────────────────────────────────────────────

/// <summary>
/// LockN Auth provider — identity, authorization, multi-tenancy, agent identity.
/// </summary>
public interface ILocknAuth : ILocknModule
{
    // ── Authentication ──────────────────────────────────────────────

    /// <summary>Authenticate and obtain tokens.</summary>
    Task<LocknResult<AuthToken>> AuthenticateAsync(
        AuthenticateRequest request, CancellationToken ct = default);

    /// <summary>Validate a token and extract identity.</summary>
    Task<LocknResult<LocknIdentity>> ValidateTokenAsync(
        string token, CancellationToken ct = default);

    /// <summary>Refresh an expired token.</summary>
    Task<LocknResult<AuthToken>> RefreshTokenAsync(
        string refreshToken, CancellationToken ct = default);

    /// <summary>Revoke a token.</summary>
    Task<LocknResult<bool>> RevokeTokenAsync(
        string token, CancellationToken ct = default);

    // ── Authorization ───────────────────────────────────────────────

    /// <summary>Check if identity has permission for a resource+action.</summary>
    Task<bool> AuthorizeAsync(
        string subjectId, string resource, string action,
        CancellationToken ct = default);

    /// <summary>Get all permissions for a subject.</summary>
    Task<IReadOnlyList<string>> GetPermissionsAsync(
        string subjectId, CancellationToken ct = default);

    /// <summary>Assign a role to a subject.</summary>
    Task<LocknResult<bool>> AssignRoleAsync(
        string subjectId, string role, CancellationToken ct = default);

    // ── Agent Identity ──────────────────────────────────────────────

    /// <summary>Create a service/agent identity for machine-to-machine auth.</summary>
    Task<LocknResult<LocknIdentity>> CreateAgentIdentityAsync(
        string name, IReadOnlyList<string> scopes, CancellationToken ct = default);

    /// <summary>Issue a delegation grant (agent acts on behalf of user).</summary>
    Task<LocknResult<DelegationGrant>> CreateDelegationAsync(
        string grantorId, string delegateId, IReadOnlyList<string> scopes,
        TimeSpan? ttl = null, CancellationToken ct = default);

    // ── Multi-Tenancy ───────────────────────────────────────────────

    /// <summary>Get tenant info.</summary>
    Task<LocknResult<Tenant>> GetTenantAsync(
        string tenantId, CancellationToken ct = default);

    /// <summary>Resolve tenant from request context (domain, header, etc.).</summary>
    Task<LocknResult<Tenant>> ResolveTenantAsync(
        string hint, CancellationToken ct = default);

    // ── Events ──────────────────────────────────────────────────────

    IObservable<AuthenticationSucceededEvent> OnAuthSuccess { get; }
    IObservable<AuthenticationFailedEvent> OnAuthFailure { get; }
    IObservable<PermissionDeniedEvent> OnPermissionDenied { get; }
}
```

### 2.4 ILocknWork — Work Items & Project Management

```csharp
namespace LockN.Abstractions.Work;

// ── Models ──────────────────────────────────────────────────────────

public record WorkIssue
{
    public required string Id { get; init; }
    public required string Identifier { get; init; }        // e.g., "LOCKN-123"
    public required string Title { get; init; }
    public string? Description { get; init; }
    public required WorkIssueState State { get; init; }
    public WorkPriority Priority { get; init; }
    public string? AssigneeId { get; init; }
    public string? ProjectId { get; init; }
    public string? CycleId { get; init; }
    public string? ParentId { get; init; }
    public int? Estimate { get; init; }
    public DateOnly? DueDate { get; init; }
    public IReadOnlyList<string> LabelIds { get; init; } = [];
    public DateTimeOffset CreatedAt { get; init; }
    public DateTimeOffset UpdatedAt { get; init; }
    public Dictionary<string, object> ProviderMetadata { get; init; } = [];
}

public record WorkIssueState(string Id, string Name, string Type); // Type: backlog, unstarted, started, completed, cancelled

public enum WorkPriority { None = 0, Urgent = 1, High = 2, Normal = 3, Low = 4 }

public record WorkProject
{
    public required string Id { get; init; }
    public required string Name { get; init; }
    public string? Description { get; init; }
    public string? LeadId { get; init; }
    public string? State { get; init; }
    public DateOnly? StartDate { get; init; }
    public DateOnly? TargetDate { get; init; }
    public double Progress { get; init; }
}

public record WorkCycle
{
    public required string Id { get; init; }
    public required string Name { get; init; }
    public required int Number { get; init; }
    public DateOnly StartDate { get; init; }
    public DateOnly EndDate { get; init; }
}

public record WorkLabel(string Id, string Name, string? Color);

public record WorkComment
{
    public required string Id { get; init; }
    public required string IssueId { get; init; }
    public required string Body { get; init; }
    public required string AuthorId { get; init; }
    public DateTimeOffset CreatedAt { get; init; }
}

public record CreateIssueRequest
{
    public required string Title { get; init; }
    public string? Description { get; init; }
    public string? TeamId { get; init; }
    public string? AssigneeId { get; init; }
    public string? ProjectId { get; init; }
    public WorkPriority? Priority { get; init; }
    public IReadOnlyList<string>? LabelIds { get; init; }
    public DateOnly? DueDate { get; init; }
}

public record UpdateIssueRequest
{
    public string? Title { get; init; }
    public string? Description { get; init; }
    public string? StateId { get; init; }
    public string? AssigneeId { get; init; }
    public WorkPriority? Priority { get; init; }
    public IReadOnlyList<string>? LabelIds { get; init; }
}

public record IssueFilter
{
    public string? AssigneeId { get; init; }
    public string? ProjectId { get; init; }
    public string? CycleId { get; init; }
    public string? StateType { get; init; }
    public WorkPriority? Priority { get; init; }
    public string? Query { get; init; }
    public int Limit { get; init; } = 50;
    public string? Cursor { get; init; }
}

// ── Events ──────────────────────────────────────────────────────────

public record IssueCreatedEvent : LocknEvent<WorkIssue>;
public record IssueUpdatedEvent : LocknEvent<(WorkIssue Issue, IReadOnlyList<string> ChangedFields)>;
public record IssueCommentedEvent : LocknEvent<WorkComment>;
public record IssueAssignedEvent : LocknEvent<(string IssueId, string? OldAssignee, string? NewAssignee)>;
public record IssueStateChangedEvent : LocknEvent<(string IssueId, WorkIssueState OldState, WorkIssueState NewState)>;

// ── Configuration ───────────────────────────────────────────────────

public class LocknWorkOptions
{
    public const string SectionName = "LockN:Work";
    public required string Provider { get; set; }           // "linear" | "plane"
    public required string ApiKey { get; set; }
    public string? TeamId { get; set; }
    public string? WebhookSecret { get; set; }
    public string? BaseUrl { get; set; }                     // For self-hosted Plane
}

// ── Interface ───────────────────────────────────────────────────────

/// <summary>
/// LockN Work provider — issues, projects, cycles, labels, assignments.
/// </summary>
public interface ILocknWork : ILocknModule
{
    // ── Issues ──────────────────────────────────────────────────────

    /// <summary>Create a new issue.</summary>
    Task<LocknResult<WorkIssue>> CreateIssueAsync(
        CreateIssueRequest request, CancellationToken ct = default);

    /// <summary>Get an issue by ID or identifier.</summary>
    Task<LocknResult<WorkIssue>> GetIssueAsync(
        string issueId, CancellationToken ct = default);

    /// <summary>Update an existing issue.</summary>
    Task<LocknResult<WorkIssue>> UpdateIssueAsync(
        string issueId, UpdateIssueRequest request, CancellationToken ct = default);

    /// <summary>List issues with filters.</summary>
    Task<PagedResult<WorkIssue>> ListIssuesAsync(
        IssueFilter filter, CancellationToken ct = default);

    /// <summary>Search issues by text query.</summary>
    Task<PagedResult<WorkIssue>> SearchIssuesAsync(
        string query, int limit = 20, CancellationToken ct = default);

    // ── Comments ────────────────────────────────────────────────────

    /// <summary>Add a comment to an issue.</summary>
    Task<LocknResult<WorkComment>> AddCommentAsync(
        string issueId, string body, CancellationToken ct = default);

    /// <summary>List comments on an issue.</summary>
    Task<PagedResult<WorkComment>> ListCommentsAsync(
        string issueId, CancellationToken ct = default);

    // ── Projects & Cycles ───────────────────────────────────────────

    Task<PagedResult<WorkProject>> ListProjectsAsync(
        int limit = 50, string? cursor = null, CancellationToken ct = default);

    Task<LocknResult<WorkProject>> GetProjectAsync(
        string projectId, CancellationToken ct = default);

    Task<PagedResult<WorkCycle>> ListCyclesAsync(
        string? teamId = null, CancellationToken ct = default);

    // ── Labels ──────────────────────────────────────────────────────

    Task<PagedResult<WorkLabel>> ListLabelsAsync(CancellationToken ct = default);

    // ── Webhooks / Events ───────────────────────────────────────────

    /// <summary>Process an incoming webhook payload from the provider.</summary>
    Task ProcessWebhookAsync(string payload, string? signature, CancellationToken ct = default);

    IObservable<IssueCreatedEvent> OnIssueCreated { get; }
    IObservable<IssueUpdatedEvent> OnIssueUpdated { get; }
    IObservable<IssueStateChangedEvent> OnIssueStateChanged { get; }
    IObservable<IssueCommentedEvent> OnIssueCommented { get; }
}
```

### 2.5 ILocknDoc — Knowledge & Documents

```csharp
namespace LockN.Abstractions.Doc;

// ── Models ──────────────────────────────────────────────────────────

public record Document
{
    public required string Id { get; init; }
    public required string Title { get; init; }
    public string? Content { get; init; }                   // Markdown
    public string? ParentId { get; init; }
    public string? WorkspaceId { get; init; }
    public string? Icon { get; init; }
    public DateTimeOffset CreatedAt { get; init; }
    public DateTimeOffset UpdatedAt { get; init; }
    public string? CreatedById { get; init; }
    public IReadOnlyList<DocumentBlock> Blocks { get; init; } = [];
    public Dictionary<string, object> Properties { get; init; } = [];
}

public record DocumentBlock
{
    public required string Id { get; init; }
    public required string Type { get; init; }              // paragraph, heading, code, image, etc.
    public required string Content { get; init; }
    public IReadOnlyList<DocumentBlock> Children { get; init; } = [];
    public Dictionary<string, object> Properties { get; init; } = [];
}

public record DocumentSearchResult
{
    public required string DocumentId { get; init; }
    public required string Title { get; init; }
    public required string Snippet { get; init; }
    public double Score { get; init; }
}

public record CreateDocumentRequest
{
    public required string Title { get; init; }
    public string? Content { get; init; }
    public string? ParentId { get; init; }
    public string? WorkspaceId { get; init; }
    public string? Icon { get; init; }
    public Dictionary<string, object>? Properties { get; init; }
}

// ── Events ──────────────────────────────────────────────────────────

public record DocumentCreatedEvent : LocknEvent<Document>;
public record DocumentUpdatedEvent : LocknEvent<Document>;
public record DocumentDeletedEvent : LocknEvent<string>;

// ── Configuration ───────────────────────────────────────────────────

public class LocknDocOptions
{
    public const string SectionName = "LockN:Doc";
    public required string Provider { get; set; }           // "notion" | "affine"
    public string? ApiKey { get; set; }
    public string? BaseUrl { get; set; }
    public string? DefaultWorkspaceId { get; set; }
}

// ── Interface ───────────────────────────────────────────────────────

/// <summary>
/// LockN Doc provider — documents, blocks, search, templates.
/// </summary>
public interface ILocknDoc : ILocknModule
{
    /// <summary>Create a new document.</summary>
    Task<LocknResult<Document>> CreateDocumentAsync(
        CreateDocumentRequest request, CancellationToken ct = default);

    /// <summary>Get a document by ID.</summary>
    Task<LocknResult<Document>> GetDocumentAsync(
        string documentId, CancellationToken ct = default);

    /// <summary>Update a document's content.</summary>
    Task<LocknResult<Document>> UpdateDocumentAsync(
        string documentId, string? title = null, string? content = null,
        CancellationToken ct = default);

    /// <summary>Delete (archive) a document.</summary>
    Task<LocknResult<bool>> DeleteDocumentAsync(
        string documentId, CancellationToken ct = default);

    /// <summary>List documents.</summary>
    Task<PagedResult<Document>> ListDocumentsAsync(
        string? parentId = null, int limit = 50, string? cursor = null,
        CancellationToken ct = default);

    /// <summary>Full-text search across documents.</summary>
    Task<PagedResult<DocumentSearchResult>> SearchAsync(
        string query, int limit = 20, CancellationToken ct = default);

    /// <summary>Append a block to a document.</summary>
    Task<LocknResult<DocumentBlock>> AppendBlockAsync(
        string documentId, DocumentBlock block, CancellationToken ct = default);

    /// <summary>Get the block children of a document or block.</summary>
    Task<IReadOnlyList<DocumentBlock>> GetBlocksAsync(
        string blockId, CancellationToken ct = default);

    IObservable<DocumentCreatedEvent> OnDocumentCreated { get; }
    IObservable<DocumentUpdatedEvent> OnDocumentUpdated { get; }
}
```

### 2.6 ILocknMem — Vector Memory

```csharp
namespace LockN.Abstractions.Mem;

// ── Models ──────────────────────────────────────────────────────────

public record MemoryCollection
{
    public required string Name { get; init; }
    public int VectorSize { get; init; }
    public DistanceMetric Distance { get; init; }
    public long PointCount { get; init; }
}

public enum DistanceMetric { Cosine, Euclidean, DotProduct }

public record MemoryPoint
{
    public required string Id { get; init; }
    public required float[] Vector { get; init; }
    public Dictionary<string, object> Payload { get; init; } = [];
}

public record MemorySearchResult
{
    public required string Id { get; init; }
    public required double Score { get; init; }
    public Dictionary<string, object> Payload { get; init; } = [];
}

public record UpsertPointRequest
{
    public required string Id { get; init; }
    public float[]? Vector { get; init; }                   // null = auto-embed from Text
    public string? Text { get; init; }                      // raw text to embed
    public Dictionary<string, object> Payload { get; init; } = [];
}

public record MemorySearchRequest
{
    public required string Collection { get; init; }
    public float[]? Vector { get; init; }                   // null = auto-embed from Query
    public string? Query { get; init; }                     // text query to embed
    public int Limit { get; init; } = 10;
    public double? ScoreThreshold { get; init; }
    public Dictionary<string, object>? Filter { get; init; }
}

// ── Events ──────────────────────────────────────────────────────────

public record PointsUpsertedEvent : LocknEvent<(string Collection, int Count)>;
public record CollectionCreatedEvent : LocknEvent<MemoryCollection>;

// ── Configuration ───────────────────────────────────────────────────

public class LocknMemOptions
{
    public const string SectionName = "LockN:Mem";
    public required string Provider { get; set; }           // "qdrant"
    public string? Endpoint { get; set; }                   // auto from Aspire service discovery
    public string? ApiKey { get; set; }
    public string? EmbeddingModel { get; set; }             // e.g., "text-embedding-3-small"
    public string? EmbeddingEndpoint { get; set; }          // OpenAI / local embedder
    public int DefaultVectorSize { get; set; } = 1536;
}

// ── Interface ───────────────────────────────────────────────────────

/// <summary>
/// LockN Mem provider — vector storage, search, embeddings.
/// </summary>
public interface ILocknMem : ILocknModule
{
    // ── Collections ─────────────────────────────────────────────────

    /// <summary>Create a vector collection.</summary>
    Task<LocknResult<MemoryCollection>> CreateCollectionAsync(
        string name, int vectorSize, DistanceMetric distance = DistanceMetric.Cosine,
        CancellationToken ct = default);

    /// <summary>List collections.</summary>
    Task<IReadOnlyList<MemoryCollection>> ListCollectionsAsync(
        CancellationToken ct = default);

    /// <summary>Delete a collection.</summary>
    Task<LocknResult<bool>> DeleteCollectionAsync(
        string name, CancellationToken ct = default);

    // ── Points ──────────────────────────────────────────────────────

    /// <summary>Upsert points (vectors + payloads). Auto-embeds if Text is provided.</summary>
    Task<LocknResult<int>> UpsertAsync(
        string collection, IReadOnlyList<UpsertPointRequest> points,
        CancellationToken ct = default);

    /// <summary>Get a point by ID.</summary>
    Task<LocknResult<MemoryPoint>> GetPointAsync(
        string collection, string pointId, CancellationToken ct = default);

    /// <summary>Delete points by IDs.</summary>
    Task<LocknResult<int>> DeletePointsAsync(
        string collection, IReadOnlyList<string> pointIds,
        CancellationToken ct = default);

    // ── Search ──────────────────────────────────────────────────────

    /// <summary>Semantic search. Auto-embeds if Query is provided instead of Vector.</summary>
    Task<IReadOnlyList<MemorySearchResult>> SearchAsync(
        MemorySearchRequest request, CancellationToken ct = default);

    // ── Embeddings ──────────────────────────────────────────────────

    /// <summary>Generate embeddings for text. Used internally but exposed for flexibility.</summary>
    Task<float[]> EmbedAsync(string text, CancellationToken ct = default);

    /// <summary>Batch embed multiple texts.</summary>
    Task<IReadOnlyList<float[]>> EmbedBatchAsync(
        IReadOnlyList<string> texts, CancellationToken ct = default);

    IObservable<PointsUpsertedEvent> OnPointsUpserted { get; }
}
```

### 2.7 ILocknArch — Architectural Diagrams

```csharp
namespace LockN.Abstractions.Arch;

// ── Models ──────────────────────────────────────────────────────────

public record Diagram
{
    public required string Id { get; init; }
    public required string Name { get; init; }
    public required DiagramFormat Format { get; init; }     // D2, Mermaid
    public required string Source { get; init; }            // Raw diagram source code
    public string? SvgContent { get; init; }
    public string? PngUrl { get; init; }
    public DateTimeOffset CreatedAt { get; init; }
    public DateTimeOffset UpdatedAt { get; init; }
}

public enum DiagramFormat { D2, Mermaid }
public enum RenderOutputFormat { Svg, Png, Pdf }

public record RenderRequest
{
    public required string Source { get; init; }
    public required DiagramFormat Format { get; init; }
    public RenderOutputFormat Output { get; init; } = RenderOutputFormat.Svg;
    public string? Theme { get; init; }
    public int? Width { get; init; }
}

// ── Configuration ───────────────────────────────────────────────────

public class LocknArchOptions
{
    public const string SectionName = "LockN:Arch";
    public required string Provider { get; set; }           // "d2" | "mermaid"
    public string? D2BinaryPath { get; set; }
    public string? Theme { get; set; }
    public string? StoragePath { get; set; }
}

// ── Interface ───────────────────────────────────────────────────────

/// <summary>
/// LockN Arch provider — diagram generation and rendering.
/// </summary>
public interface ILocknArch : ILocknModule
{
    /// <summary>Render a diagram from source code.</summary>
    Task<LocknResult<byte[]>> RenderAsync(
        RenderRequest request, CancellationToken ct = default);

    /// <summary>Save a diagram (source + rendered output).</summary>
    Task<LocknResult<Diagram>> SaveDiagramAsync(
        string name, string source, DiagramFormat format,
        CancellationToken ct = default);

    /// <summary>Get a saved diagram.</summary>
    Task<LocknResult<Diagram>> GetDiagramAsync(
        string diagramId, CancellationToken ct = default);

    /// <summary>List saved diagrams.</summary>
    Task<PagedResult<Diagram>> ListDiagramsAsync(
        int limit = 50, string? cursor = null, CancellationToken ct = default);

    /// <summary>Validate diagram source without rendering.</summary>
    Task<LocknResult<bool>> ValidateAsync(
        string source, DiagramFormat format, CancellationToken ct = default);
}
```

### 2.8 ILocknFlow — Workflow Orchestration

```csharp
namespace LockN.Abstractions.Flow;

// ── Models ──────────────────────────────────────────────────────────

public record WorkflowDefinition
{
    public required string Name { get; init; }
    public required string TaskQueue { get; init; }
    public string? Description { get; init; }
    public TimeSpan? ExecutionTimeout { get; init; }
    public RetryPolicy? RetryPolicy { get; init; }
}

public record WorkflowExecution
{
    public required string WorkflowId { get; init; }
    public required string RunId { get; init; }
    public required string WorkflowName { get; init; }
    public required WorkflowStatus Status { get; init; }
    public DateTimeOffset StartedAt { get; init; }
    public DateTimeOffset? CompletedAt { get; init; }
    public object? Result { get; init; }
    public string? Error { get; init; }
}

public enum WorkflowStatus { Running, Completed, Failed, Cancelled, TimedOut, Terminated }

public record RetryPolicy
{
    public int MaxRetries { get; init; } = 3;
    public TimeSpan InitialInterval { get; init; } = TimeSpan.FromSeconds(1);
    public double BackoffCoefficient { get; init; } = 2.0;
    public TimeSpan? MaxInterval { get; init; }
}

public record StartWorkflowRequest
{
    public required string WorkflowName { get; init; }
    public string? WorkflowId { get; init; }                // Client-assigned; auto-generated if null
    public required string TaskQueue { get; init; }
    public object? Input { get; init; }
    public TimeSpan? ExecutionTimeout { get; init; }
    public Dictionary<string, string>? SearchAttributes { get; init; }
}

public record SignalRequest
{
    public required string WorkflowId { get; init; }
    public required string SignalName { get; init; }
    public object? Input { get; init; }
}

public record QueryRequest
{
    public required string WorkflowId { get; init; }
    public required string QueryName { get; init; }
    public object? Args { get; init; }
}

// ── Events ──────────────────────────────────────────────────────────

public record WorkflowStartedEvent : LocknEvent<WorkflowExecution>;
public record WorkflowCompletedEvent : LocknEvent<WorkflowExecution>;
public record WorkflowFailedEvent : LocknEvent<(WorkflowExecution Execution, string Error)>;

// ── Configuration ───────────────────────────────────────────────────

public class LocknFlowOptions
{
    public const string SectionName = "LockN:Flow";
    public required string Provider { get; set; }           // "temporal"
    public required string Endpoint { get; set; }           // Auto from Aspire
    public string Namespace { get; set; } = "default";
    public string DefaultTaskQueue { get; set; } = "lockn-main";
}

// ── Interface ───────────────────────────────────────────────────────

/// <summary>
/// LockN Flow provider — workflow definition, execution, signals, queries.
/// </summary>
public interface ILocknFlow : ILocknModule
{
    /// <summary>Start a new workflow execution.</summary>
    Task<LocknResult<WorkflowExecution>> StartWorkflowAsync(
        StartWorkflowRequest request, CancellationToken ct = default);

    /// <summary>Get workflow execution status.</summary>
    Task<LocknResult<WorkflowExecution>> GetWorkflowAsync(
        string workflowId, CancellationToken ct = default);

    /// <summary>List workflow executions.</summary>
    Task<PagedResult<WorkflowExecution>> ListWorkflowsAsync(
        string? query = null, int limit = 50, string? cursor = null,
        CancellationToken ct = default);

    /// <summary>Send a signal to a running workflow.</summary>
    Task<LocknResult<bool>> SignalWorkflowAsync(
        SignalRequest request, CancellationToken ct = default);

    /// <summary>Query a running workflow for its current state.</summary>
    Task<LocknResult<object>> QueryWorkflowAsync(
        QueryRequest request, CancellationToken ct = default);

    /// <summary>Cancel a running workflow.</summary>
    Task<LocknResult<bool>> CancelWorkflowAsync(
        string workflowId, CancellationToken ct = default);

    /// <summary>Terminate a running workflow immediately.</summary>
    Task<LocknResult<bool>> TerminateWorkflowAsync(
        string workflowId, string reason, CancellationToken ct = default);

    /// <summary>Wait for workflow completion and return result.</summary>
    Task<LocknResult<T>> GetWorkflowResultAsync<T>(
        string workflowId, CancellationToken ct = default);

    IObservable<WorkflowStartedEvent> OnWorkflowStarted { get; }
    IObservable<WorkflowCompletedEvent> OnWorkflowCompleted { get; }
    IObservable<WorkflowFailedEvent> OnWorkflowFailed { get; }
}
```

### 2.9 ILocknWatch — Observability

```csharp
namespace LockN.Abstractions.Watch;

// ── Models ──────────────────────────────────────────────────────────

public record MetricDefinition
{
    public required string Name { get; init; }
    public required string Unit { get; init; }
    public required MetricType Type { get; init; }
    public string? Description { get; init; }
    public Dictionary<string, string> Tags { get; init; } = [];
}

public enum MetricType { Counter, Gauge, Histogram }

public record AlertRule
{
    public required string Id { get; init; }
    public required string Name { get; init; }
    public required string Expression { get; init; }        // PromQL or OTel compatible
    public required AlertSeverity Severity { get; init; }
    public TimeSpan EvaluationInterval { get; init; }
    public string? NotificationChannel { get; init; }       // Chat channel ID
}

public enum AlertSeverity { Info, Warning, Critical }

public record AlertEvent : LocknEvent<AlertRule>;

// ── Configuration ───────────────────────────────────────────────────

public class LocknWatchOptions
{
    public const string SectionName = "LockN:Watch";
    public string? OtlpEndpoint { get; set; }               // Auto from Aspire
    public string? GrafanaUrl { get; set; }
    public string? GrafanaApiKey { get; set; }
    public bool EnableAspireDashboard { get; set; } = true;
}

// ── Interface ───────────────────────────────────────────────────────

/// <summary>
/// LockN Watch provider — metrics, traces, logs, alerts.
/// Mostly a thin layer over OTel; provides LockN-specific metric recording and alert management.
/// </summary>
public interface ILocknWatch : ILocknModule
{
    // ── Metrics ─────────────────────────────────────────────────────

    /// <summary>Record a counter increment.</summary>
    void RecordCounter(string name, long value = 1, params KeyValuePair<string, object?>[] tags);

    /// <summary>Record a gauge value.</summary>
    void RecordGauge(string name, double value, params KeyValuePair<string, object?>[] tags);

    /// <summary>Record a histogram observation.</summary>
    void RecordHistogram(string name, double value, params KeyValuePair<string, object?>[] tags);

    // ── Alerts ──────────────────────────────────────────────────────

    /// <summary>Create or update an alert rule.</summary>
    Task<LocknResult<AlertRule>> UpsertAlertRuleAsync(
        AlertRule rule, CancellationToken ct = default);

    /// <summary>List active alert rules.</summary>
    Task<IReadOnlyList<AlertRule>> ListAlertRulesAsync(CancellationToken ct = default);

    /// <summary>Delete an alert rule.</summary>
    Task<LocknResult<bool>> DeleteAlertRuleAsync(
        string ruleId, CancellationToken ct = default);

    // ── Events ──────────────────────────────────────────────────────

    IObservable<AlertEvent> OnAlert { get; }
}
```

### 2.10 ILocknVoice — Text-to-Speech & Voice

```csharp
namespace LockN.Abstractions.Voice;

// ── Models ──────────────────────────────────────────────────────────

public record VoiceProfile
{
    public required string Id { get; init; }
    public required string Name { get; init; }
    public string? Description { get; init; }
    public string? Language { get; init; }
    public string? SampleUrl { get; init; }
}

public record SynthesisRequest
{
    public required string Text { get; init; }
    public string? VoiceId { get; init; }
    public string? Language { get; init; }
    public double Speed { get; init; } = 1.0;
    public AudioFormat Format { get; init; } = AudioFormat.Mp3;
}

public enum AudioFormat { Mp3, Wav, Ogg, Pcm }

public record TranscriptionResult
{
    public required string Text { get; init; }
    public string? Language { get; init; }
    public double Confidence { get; init; }
    public IReadOnlyList<WordTimestamp> Words { get; init; } = [];
}

public record WordTimestamp(string Word, TimeSpan Start, TimeSpan End);

// ── Configuration ───────────────────────────────────────────────────

public class LocknVoiceOptions
{
    public const string SectionName = "LockN:Voice";
    public required string Provider { get; set; }           // "fish-speech" | "elevenlabs"
    public string? ApiKey { get; set; }
    public string? BaseUrl { get; set; }                     // Fish Speech local endpoint
    public string? DefaultVoiceId { get; set; }
}

// ── Interface ───────────────────────────────────────────────────────

/// <summary>
/// LockN Voice provider — TTS, STT, voice cloning, streaming.
/// </summary>
public interface ILocknVoice : ILocknModule
{
    // ── Text-to-Speech ──────────────────────────────────────────────

    /// <summary>Synthesize text to audio bytes.</summary>
    Task<LocknResult<byte[]>> SynthesizeAsync(
        SynthesisRequest request, CancellationToken ct = default);

    /// <summary>Stream synthesized audio chunks (for real-time playback).</summary>
    IAsyncEnumerable<byte[]> SynthesizeStreamAsync(
        SynthesisRequest request, CancellationToken ct = default);

    // ── Speech-to-Text ──────────────────────────────────────────────

    /// <summary>Transcribe audio to text.</summary>
    Task<LocknResult<TranscriptionResult>> TranscribeAsync(
        Stream audioStream, string? language = null,
        CancellationToken ct = default);

    /// <summary>Stream transcription results as audio is received.</summary>
    IAsyncEnumerable<TranscriptionResult> TranscribeStreamAsync(
        IAsyncEnumerable<byte[]> audioChunks, string? language = null,
        CancellationToken ct = default);

    // ── Voice Profiles ──────────────────────────────────────────────

    /// <summary>List available voice profiles.</summary>
    Task<IReadOnlyList<VoiceProfile>> ListVoicesAsync(
        CancellationToken ct = default);

    /// <summary>Clone a voice from audio samples.</summary>
    Task<LocknResult<VoiceProfile>> CloneVoiceAsync(
        string name, Stream audioSample, CancellationToken ct = default);
}
```

---

## 3. Service Discovery & Communication

### 3.1 Aspire's Built-in Service Discovery

Aspire automatically injects connection strings and service endpoints as environment variables. Services reference each other by name:

```csharp
// In any service's Program.cs:
builder.AddServiceDefaults();

// HttpClient gets automatic service discovery:
builder.Services.AddHttpClient<IChatApi>(client =>
{
    client.BaseAddress = new Uri("https+http://chat-service");
});

// Named Qdrant client auto-resolves:
builder.AddQdrantClient("qdrant");
```

**Environment variable injection:**
- `ConnectionStrings__qdrant=http://localhost:6334`
- `services__chat-service__https__0=https://localhost:5201`

### 3.2 Communication Patterns

| Communication | Protocol | Use Case |
|---|---|---|
| **Service → Service** | gRPC (Protobuf) | High-perf internal calls (Mem search, Flow signals) |
| **Gateway → Services** | REST (JSON) | API gateway to internal services |
| **OpenClaw → Gateway** | REST (JSON) | Node.js runtime calling .NET via Gateway |
| **Gateway → OpenClaw** | REST (JSON) + WebSocket | Push events, agent commands |
| **Event Bus** | Redis Streams | Cross-module events, webhooks fan-out |
| **Service → Temporal** | gRPC (Temporal SDK) | Workflow orchestration |

### 3.3 OpenClaw ↔ .NET Communication

```
┌─────────────┐     REST/JSON      ┌──────────────┐     gRPC      ┌──────────────┐
│  OpenClaw    │ ◄──────────────► │  LockN       │ ◄──────────► │  Chat/Work/  │
│  (Node.js)  │                    │  Gateway     │               │  Mem/etc.    │
└─────────────┘                    └──────────────┘               └──────────────┘
       │                                  │
       │         Redis Streams            │
       └──────────────────────────────────┘
                (Event bus)
```

**Gateway exposes a unified REST API:**

```
POST   /api/chat/send
GET    /api/work/issues/{id}
POST   /api/mem/search
POST   /api/flow/workflows
POST   /api/voice/synthesize
```

OpenClaw calls these endpoints. The Gateway routes to internal gRPC services via Aspire service discovery.

### 3.4 Event Flow Between Modules

```
Chat.MessageReceived → Mem.StoreContext (auto-embed conversations)
Chat.MessageReceived → Flow.TriggerWorkflow (agent command detection)
Work.IssueStateChanged → Chat.SendNotification
Work.IssueCreated → Mem.StoreContext
Flow.WorkflowCompleted → Chat.SendResult
Auth.PermissionDenied → Watch.RecordMetric → Watch.AlertIfThreshold
Voice.Synthesized → Chat.SendAudioMessage
Doc.DocumentUpdated → Mem.ReindexDocument
```

Events flow via **Redis Streams** with the following pattern:

```csharp
// Publishing (in any provider):
await _eventBus.PublishAsync("lockn.chat.message_received", messageEvent);

// Subscribing (in consuming service):
_eventBus.Subscribe<MessageReceivedEvent>("lockn.chat.message_received",
    async (evt) => await _mem.UpsertAsync("conversations", ...));
```

### 3.5 Event Bus Abstraction

```csharp
namespace LockN.Abstractions.Common;

/// <summary>
/// Internal event bus for cross-module communication.
/// Default implementation: Redis Streams.
/// </summary>
public interface ILocknEventBus
{
    Task PublishAsync<T>(string topic, T payload, CancellationToken ct = default)
        where T : LocknEvent;

    IDisposable Subscribe<T>(string topic, Func<T, Task> handler)
        where T : LocknEvent;

    IObservable<T> Observe<T>(string topic) where T : LocknEvent;
}
```

---

## 4. Dependency Injection & Provider Registration

### 4.1 Registration Pattern

Each provider ships extension methods:

```csharp
namespace LockN.Chat.Matrix;

public static class MatrixChatExtensions
{
    /// <summary>Register Matrix as the ILocknChat provider.</summary>
    public static IServiceCollection AddLocknChatMatrix(
        this IServiceCollection services,
        Action<LocknChatOptions>? configure = null)
    {
        services.AddOptions<LocknChatOptions>()
            .BindConfiguration(LocknChatOptions.SectionName)
            .ValidateDataAnnotations()
            .ValidateOnStart();

        if (configure is not null)
            services.Configure(configure);

        services.AddSingleton<ILocknChat, MatrixChatProvider>();
        services.AddHostedService<MatrixSyncService>();     // Background sync loop

        return services;
    }
}
```

**Usage in a service's `Program.cs`:**

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.AddServiceDefaults();

// Provider selected by config or explicit registration:
builder.Services.AddLocknChatMatrix();
// — OR —
builder.Services.AddLocknChatSlack();
```

### 4.2 Configuration-Driven Provider Swapping

```jsonc
// appsettings.json
{
  "LockN": {
    "Chat": {
      "Provider": "matrix",
      "HomeserverUrl": "https://matrix.lockn.ai",
      "AccessToken": "syt_...",
      "BotUserId": "@lockn:lockn.ai"
    },
    "Auth": {
      "Provider": "zitadel",
      "Authority": "https://auth.lockn.ai",
      "Audience": "lockn-api"
    },
    "Work": {
      "Provider": "linear",
      "ApiKey": "lin_api_..."
    },
    "Mem": {
      "Provider": "qdrant",
      "EmbeddingModel": "text-embedding-3-small"
    }
  }
}
```

**Factory pattern for config-driven registration:**

```csharp
public static class LocknChatFactory
{
    public static IServiceCollection AddLocknChat(
        this IServiceCollection services, IConfiguration config)
    {
        var provider = config.GetValue<string>("LockN:Chat:Provider");
        return provider switch
        {
            "matrix" => services.AddLocknChatMatrix(),
            "slack"  => services.AddLocknChatSlack(),
            _ => throw new InvalidOperationException($"Unknown chat provider: {provider}")
        };
    }
}
```

### 4.3 Multi-Provider / Bridge Scenarios

For running multiple providers simultaneously (e.g., bridging Slack ↔ Matrix):

```csharp
// Register keyed services (.NET 8+):
services.AddKeyedSingleton<ILocknChat, MatrixChatProvider>("matrix");
services.AddKeyedSingleton<ILocknChat, SlackChatProvider>("slack");

// Bridge coordinator uses both:
services.AddSingleton<ChatBridge>(sp => new ChatBridge(
    primary: sp.GetRequiredKeyedService<ILocknChat>("matrix"),
    secondary: sp.GetRequiredKeyedService<ILocknChat>("slack")
));

// Default ILocknChat resolves to the primary:
services.AddSingleton<ILocknChat>(sp =>
    sp.GetRequiredKeyedService<ILocknChat>("matrix"));
```

---

## 5. OpenTelemetry Integration

### 5.1 How Aspire Wires OTel

Aspire's `ServiceDefaults` project configures OTel automatically. The Aspire dashboard at `https://localhost:18888` shows:

- **Traces** — Distributed traces across all services
- **Metrics** — Custom + system metrics
- **Logs** — Structured logs from all services

No additional Prometheus/Grafana needed for development. For production, the same OTel data exports to Grafana Cloud or self-hosted Grafana via OTLP.

### 5.2 Custom Metrics Per Module

```csharp
// In each provider, define a static Meter:
namespace LockN.Chat.Matrix;

public partial class MatrixChatProvider : ILocknChat
{
    private static readonly Meter s_meter = new("LockN.Chat", "1.0.0");
    private static readonly Counter<long> s_messagesSent =
        s_meter.CreateCounter<long>("lockn.chat.messages_sent", "messages");
    private static readonly Counter<long> s_messagesReceived =
        s_meter.CreateCounter<long>("lockn.chat.messages_received", "messages");
    private static readonly Histogram<double> s_sendLatency =
        s_meter.CreateHistogram<double>("lockn.chat.send_latency_ms", "ms");

    public async Task<LocknResult<ChatMessage>> SendMessageAsync(
        SendMessageRequest request, CancellationToken ct)
    {
        var sw = Stopwatch.StartNew();
        try
        {
            var result = await SendToMatrixAsync(request, ct);
            s_messagesSent.Add(1, new("channel", request.ChannelId));
            s_sendLatency.Record(sw.Elapsed.TotalMilliseconds);
            return result;
        }
        catch (Exception ex)
        {
            s_meter.CreateCounter<long>("lockn.chat.errors")
                .Add(1, new("operation", "send"));
            throw;
        }
    }
}
```

**Per-module custom metrics:**

| Module | Key Metrics |
|---|---|
| Chat | `messages_sent`, `messages_received`, `send_latency_ms`, `active_channels` |
| Auth | `auth_success`, `auth_failures`, `token_refreshes`, `permission_denied` |
| Work | `issues_created`, `issues_updated`, `webhook_latency_ms` |
| Mem | `vectors_upserted`, `searches_executed`, `search_latency_ms`, `embed_latency_ms` |
| Flow | `workflows_started`, `workflows_completed`, `workflows_failed`, `workflow_duration_ms` |
| Voice | `synthesis_requests`, `synthesis_latency_ms`, `audio_bytes_generated` |

### 5.3 Distributed Tracing — Agent Request Lifecycle

```
OpenClaw receives user message
  └─ POST /api/chat/send (Gateway)
       └─ gRPC ChatService.ProcessMessage
            ├─ ILocknMem.SearchAsync (context retrieval)  ── trace span
            ├─ ILocknFlow.StartWorkflow (agent reasoning) ── trace span
            │    ├─ Activity: tool_call (Linear)          ── trace span
            │    └─ Activity: tool_call (Notion)          ── trace span
            ├─ ILocknVoice.SynthesizeAsync (if voice)     ── trace span
            └─ ILocknChat.SendMessageAsync (response)     ── trace span
```

Each span carries `correlation_id` from the original message, enabling end-to-end tracing from user input to final response.

### 5.4 Grafana in Production

```
Aspire Dashboard (dev) ──→ OTLP Exporter ──→ Grafana Cloud / Self-hosted
                                               ├── Tempo (traces)
                                               ├── Loki (logs)
                                               └── Mimir (metrics)
```

The existing Prometheus+Grafana stack is **replaced** by OTel collectors exporting to the same Grafana instance. Custom dashboards import from Aspire-compatible OTel data.

---

## 6. Deployment Topology

### 6.1 Local Development

```bash
# Single command starts everything:
cd src/AppHost/LockN.AppHost
dotnet run

# Aspire dashboard: https://localhost:18888
# Gateway API:      https://localhost:5100
# OpenClaw:         http://localhost:3100
# Temporal UI:      http://localhost:8233
# Grafana:          http://localhost:3000
```

Aspire handles:
- Starting all .NET projects
- Pulling and running Docker containers (Qdrant, Dendrite, Temporal, Grafana, Redis)
- Building and running the OpenClaw Dockerfile
- Wiring service discovery environment variables
- Health checks and log aggregation

### 6.2 Docker Compose Generation (Self-Hosted)

```bash
# Generate manifest:
dotnet run --project src/AppHost/LockN.AppHost -- --publisher manifest --output-path ./deploy/manifest.json

# Use aspirate (Aspire Deploy Tool) to generate Docker Compose:
aspirate generate --manifest ./deploy/manifest.json --output ./deploy/docker-compose
```

This produces a `docker-compose.yml` with all services, containers, environment variables, volumes, and networks pre-configured.

### 6.3 Kubernetes (Enterprise)

```bash
# Generate k8s manifests:
aspirate generate --manifest ./deploy/manifest.json --output ./deploy/k8s --type kustomize
```

Produces:
- Deployments for each .NET service
- StatefulSets for Qdrant, Temporal, Dendrite
- Services with correct port mappings
- ConfigMaps for appsettings
- Secrets for API keys
- Ingress for Gateway

### 6.4 Migrating Existing Docker Containers

| Existing | Migration Path |
|---|---|
| `lockn-swap` | `.NET project → `AddProject<Projects.LockN_Swap>()` |
| `lockn-apikeys` | Same — migrates to Aspire-managed .NET project |
| `lockn-logger` | Absorbed into LockN.Watch + OTel; remove standalone container |
| `lockn-listen` | Same — Aspire-managed .NET project |

The existing containers become Aspire project references. Their Docker deployment is auto-generated by Aspire's manifest publisher.

---

## 7. NuGet Packaging Strategy

### 7.1 Package Map

| Package | Contents | Audience |
|---|---|---|
| `LockN.Abstractions` | All interfaces, DTOs, events, config models | **Everyone** — core contracts |
| `LockN.ServiceDefaults` | Aspire defaults, OTel, health checks | Internal services only |
| `LockN.Chat.Matrix` | Matrix provider implementation | Customers wanting Matrix |
| `LockN.Chat.Slack` | Slack provider implementation | Customers wanting Slack |
| `LockN.Auth.Zitadel` | Zitadel provider | — |
| `LockN.Auth.Auth0` | Auth0 provider | — |
| `LockN.Work.Linear` | Linear provider | — |
| `LockN.Work.Plane` | Plane provider | — |
| `LockN.Doc.Notion` | Notion provider | — |
| `LockN.Doc.AFFiNE` | AFFiNE provider | — |
| `LockN.Mem.Qdrant` | Qdrant provider | — |
| `LockN.Arch.D2` | D2 renderer | — |
| `LockN.Arch.Mermaid` | Mermaid renderer | — |
| `LockN.Flow.Temporal` | Temporal provider | — |
| `LockN.Voice.FishSpeech` | Fish Speech provider | — |
| `LockN.Voice.ElevenLabs` | ElevenLabs provider | — |
| `LockN.Hosting.Temporal` | Aspire hosting extension | AppHost authors |
| `LockN.Hosting.Dendrite` | Aspire hosting extension | AppHost authors |

### 7.2 Versioning Strategy

- **SemVer 2.0** for all packages
- `LockN.Abstractions` is versioned independently and follows strict backward compatibility
- Provider packages track their own version but pin a minimum `LockN.Abstractions` version
- All packages in a release train share a common **major.minor** but may differ in **patch**

```xml
<!-- Provider .csproj -->
<PackageReference Include="LockN.Abstractions" Version="[1.0.0, 2.0.0)" />
```

### 7.3 Consumption Models

**Full stack (internal / turnkey deployment):**
```bash
dotnet add package LockN.Abstractions
dotnet add package LockN.Chat.Matrix
dotnet add package LockN.Auth.Zitadel
dotnet add package LockN.Work.Linear
dotnet add package LockN.Mem.Qdrant
# ... etc
```

**Individual module (customer integrating just one capability):**
```bash
dotnet add package LockN.Abstractions
dotnet add package LockN.Mem.Qdrant
# Customer only uses vector memory
```

**Custom provider (customer building their own):**
```bash
dotnet add package LockN.Abstractions
# Implement ILocknChat for their internal system
```

### 7.4 NuGet Feed

- **Private feed** during development: GitHub Packages or Azure Artifacts
- **Public NuGet.org** when ready for GA
- CI/CD publishes pre-release packages on every merge to `main`:
  - `LockN.Abstractions 1.0.0-preview.42`

---

## Appendix A: Technology Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Orchestrator | .NET Aspire | Unified local dev, service discovery, OTel, container management |
| Internal RPC | gRPC | Performance, codegen, streaming support |
| External API | REST/JSON | OpenClaw is Node.js; JSON is universal |
| Event bus | Redis Streams | Already in stack, lightweight, Aspire has built-in Redis integration |
| Workflow engine | Temporal | Durable execution, retry, long-running agents |
| Vector DB | Qdrant | First-class Aspire integration, gRPC, fast |
| Identity | Zitadel (primary) | Self-hosted, agent identity support, OIDC |
| Runtime | .NET 9 | LTS, Aspire support, performance |

## Appendix B: Aspire NuGet Packages Required

```xml
<!-- AppHost -->
<PackageReference Include="Aspire.Hosting.AppHost" />
<PackageReference Include="Aspire.Hosting.Redis" />
<PackageReference Include="Aspire.Hosting.Qdrant" />
<PackageReference Include="Aspire.Hosting.JavaScript" />

<!-- Service Defaults -->
<PackageReference Include="Microsoft.Extensions.Http.Resilience" />
<PackageReference Include="Microsoft.Extensions.ServiceDiscovery" />
<PackageReference Include="OpenTelemetry.Exporter.OpenTelemetryProtocol" />
<PackageReference Include="OpenTelemetry.Extensions.Hosting" />
<PackageReference Include="OpenTelemetry.Instrumentation.AspNetCore" />
<PackageReference Include="OpenTelemetry.Instrumentation.GrpcNetClient" />
<PackageReference Include="OpenTelemetry.Instrumentation.Http" />
<PackageReference Include="OpenTelemetry.Instrumentation.Runtime" />

<!-- Per-service (example: Mem service) -->
<PackageReference Include="Aspire.Qdrant.Client" />
<PackageReference Include="Grpc.AspNetCore" />
```

---

*End of architecture document. This is a living document — update as implementation progresses.*
