using System.Diagnostics;
using System.Diagnostics.Metrics;

namespace LockNGen.Infrastructure.Telemetry;

/// <summary>
/// Telemetry instrumentation for generation processing.
/// Provides ActivitySource for distributed tracing and Meter for metrics.
/// </summary>
public static class GenerationInstrumentation
{
    public const string ServiceName = "lockn-gen";
    public const string ServiceVersion = "1.0.0";
    
    /// <summary>Activity source for distributed tracing.</summary>
    public static readonly ActivitySource ActivitySource = new(ServiceName, ServiceVersion);
    
    /// <summary>Meter for custom metrics.</summary>
    public static readonly Meter Meter = new(ServiceName, ServiceVersion);
    
    // Counters
    private static readonly Counter<long> GenerationsCompleted = Meter.CreateCounter<long>(
        "generation.completed",
        description: "Number of generations completed successfully");
    
    private static readonly Counter<long> GenerationsFailed = Meter.CreateCounter<long>(
        "generation.failed",
        description: "Number of generations that failed");
    
    // Histograms
    private static readonly Histogram<double> GenerationDuration = Meter.CreateHistogram<double>(
        "generation.duration_ms",
        unit: "ms",
        description: "Duration of generation processing in milliseconds");
    
    private static readonly Histogram<double> QueueWaitTime = Meter.CreateHistogram<double>(
        "generation.queue_wait_ms",
        unit: "ms",
        description: "Time spent waiting in queue before processing");
    
    // Gauges
    private static int _activeGenerations;
    private static int _queueDepth;
    
    static GenerationInstrumentation()
    {
        Meter.CreateObservableGauge(
            "generation.active",
            () => _activeGenerations,
            description: "Number of generations currently being processed");
        
        Meter.CreateObservableGauge(
            "generation.queue_depth",
            () => _queueDepth,
            description: "Number of generations waiting in queue");
    }
    
    /// <summary>Start a traced activity for generation processing.</summary>
    public static Activity? StartProcessingActivity(Guid generationId, string model)
    {
        var activity = ActivitySource.StartActivity("generation.process", ActivityKind.Internal);
        activity?.SetTag("generation.id", generationId.ToString());
        activity?.SetTag("generation.model", model);
        return activity;
    }
    
    /// <summary>Record successful generation completion.</summary>
    public static void RecordCompletion(string model, double durationMs, double queueWaitMs)
    {
        GenerationsCompleted.Add(1, new KeyValuePair<string, object?>("model", model));
        GenerationDuration.Record(durationMs, new KeyValuePair<string, object?>("model", model));
        QueueWaitTime.Record(queueWaitMs, new KeyValuePair<string, object?>("model", model));
    }
    
    /// <summary>Record failed generation.</summary>
    public static void RecordFailure(string model, string errorType)
    {
        GenerationsFailed.Add(1,
            new KeyValuePair<string, object?>("model", model),
            new KeyValuePair<string, object?>("error_type", errorType));
    }
    
    /// <summary>Update active generations gauge.</summary>
    public static void SetActiveGenerations(int count) => Interlocked.Exchange(ref _activeGenerations, count);
    
    /// <summary>Update queue depth gauge.</summary>
    public static void SetQueueDepth(int count) => Interlocked.Exchange(ref _queueDepth, count);
    
    /// <summary>Increment active generations.</summary>
    public static void IncrementActive() => Interlocked.Increment(ref _activeGenerations);
    
    /// <summary>Decrement active generations.</summary>
    public static void DecrementActive() => Interlocked.Decrement(ref _activeGenerations);
}
