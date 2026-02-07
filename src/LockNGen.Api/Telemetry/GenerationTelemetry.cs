using System.Diagnostics;
using System.Diagnostics.Metrics;

namespace LockNGen.Api.Telemetry;

/// <summary>
/// OpenTelemetry instrumentation for generation service.
/// Provides tracing and metrics for image generation operations.
/// </summary>
public static class GenerationTelemetry
{
    public const string ServiceName = "lockn-gen";
    public const string ServiceVersion = "1.0.0";
    
    // Activity source for distributed tracing
    public static readonly ActivitySource ActivitySource = new(ServiceName, ServiceVersion);
    
    // Meter for custom metrics
    private static readonly Meter Meter = new(ServiceName, ServiceVersion);
    
    // Counters
    private static readonly Counter<long> GenerationRequestsTotal = Meter.CreateCounter<long>(
        "generation.requests.total",
        description: "Total number of generation requests received");
    
    private static readonly Counter<long> GenerationCompletedTotal = Meter.CreateCounter<long>(
        "generation.completed.total",
        description: "Total number of generations completed successfully");
    
    private static readonly Counter<long> GenerationFailedTotal = Meter.CreateCounter<long>(
        "generation.failed.total",
        description: "Total number of generations that failed");
    
    private static readonly Counter<long> GenerationCancelledTotal = Meter.CreateCounter<long>(
        "generation.cancelled.total",
        description: "Total number of generations cancelled");
    
    // Histograms
    private static readonly Histogram<double> GenerationDuration = Meter.CreateHistogram<double>(
        "generation.duration.seconds",
        unit: "s",
        description: "Duration of generation processing in seconds");
    
    private static readonly Histogram<double> GenerationQueueTime = Meter.CreateHistogram<double>(
        "generation.queue_time.seconds",
        unit: "s",
        description: "Time spent in queue before processing starts");
    
    private static readonly Histogram<double> GenerationCostEstimate = Meter.CreateHistogram<double>(
        "generation.cost.estimate",
        unit: "credits",
        description: "Estimated cost of generation in credits");
    
    // Gauges (using ObservableGauge with callbacks)
    private static int _queueDepth;
    private static int _activeGenerations;
    
    static GenerationTelemetry()
    {
        Meter.CreateObservableGauge(
            "generation.queue.depth",
            () => _queueDepth,
            description: "Current number of generations in queue");
        
        Meter.CreateObservableGauge(
            "generation.active.count",
            () => _activeGenerations,
            description: "Current number of generations being processed");
    }
    
    /// <summary>Record a new generation request.</summary>
    public static void RecordGenerationRequest(string model, int width, int height)
    {
        GenerationRequestsTotal.Add(1, 
            new KeyValuePair<string, object?>("model", model),
            new KeyValuePair<string, object?>("resolution", $"{width}x{height}"));
    }
    
    /// <summary>Record a completed generation with timing.</summary>
    public static void RecordGenerationCompleted(string model, double durationSeconds, double? queueTimeSeconds = null)
    {
        GenerationCompletedTotal.Add(1, new KeyValuePair<string, object?>("model", model));
        GenerationDuration.Record(durationSeconds, new KeyValuePair<string, object?>("model", model));
        
        if (queueTimeSeconds.HasValue)
        {
            GenerationQueueTime.Record(queueTimeSeconds.Value, new KeyValuePair<string, object?>("model", model));
        }
    }
    
    /// <summary>Record a failed generation.</summary>
    public static void RecordGenerationFailed(string model, string reason)
    {
        GenerationFailedTotal.Add(1, 
            new KeyValuePair<string, object?>("model", model),
            new KeyValuePair<string, object?>("reason", reason));
    }
    
    /// <summary>Record a cancelled generation.</summary>
    public static void RecordGenerationCancelled(string model)
    {
        GenerationCancelledTotal.Add(1, new KeyValuePair<string, object?>("model", model));
    }
    
    /// <summary>Record estimated generation cost.</summary>
    public static void RecordGenerationCost(string model, int width, int height, int steps, double costEstimate)
    {
        GenerationCostEstimate.Record(costEstimate,
            new KeyValuePair<string, object?>("model", model),
            new KeyValuePair<string, object?>("resolution", $"{width}x{height}"),
            new KeyValuePair<string, object?>("steps", steps));
    }
    
    /// <summary>Update queue depth gauge.</summary>
    public static void SetQueueDepth(int depth) => _queueDepth = depth;
    
    /// <summary>Update active generations gauge.</summary>
    public static void SetActiveGenerations(int count) => _activeGenerations = count;
    
    /// <summary>Start a traced activity for generation.</summary>
    public static Activity? StartGenerationActivity(Guid generationId, string prompt)
    {
        var activity = ActivitySource.StartActivity("generation.process", ActivityKind.Internal);
        activity?.SetTag("generation.id", generationId.ToString());
        activity?.SetTag("generation.prompt_length", prompt.Length);
        return activity;
    }
}
