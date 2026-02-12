using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using System;

/// <summary>
/// Receipt endpoints with XML documentation
/// </summary>
[ApiController]
[Route("api/[controller]")]
public class ReceiptsController : ControllerBase
{
    private readonly ILogger<ReceiptsController> _logger;

    public ReceiptsController(ILogger<ReceiptsController> logger)
    {
        _logger = logger;
    }

    /// <summary>
    /// Get all receipts
    /// </summary>
    /// <returns>Receipt collection</returns>
    [HttpGet]
    public IActionResult Get() => Ok(new[] { "receipt1", "receipt2" });

    /// <summary>
    /// Create new receipt
    /// </summary>
    /// <param name="receipt">Receipt data</param>
    /// <returns>Created receipt</returns>
    [HttpPost]
    public IActionResult Post([FromBody] string receipt) => Created($"/receipts/{receipt}", receipt);

    /// <summary>
    /// Emit decision requested receipt
    /// </summary>
    /// <param name="decisionRequest">Decision request data</param>
    /// <returns>Acknowledgment</returns>
    [HttpPost("decision-requested")]
    public IActionResult EmitDecisionRequested([FromBody] DecisionRequestedReceipt decisionRequest)
    {
        if (decisionRequest == null)
        {
            return BadRequest("Decision request data is required");
        }

        _logger.LogInformation("Decision requested receipt emitted: {CorrelationId}", decisionRequest.CorrelationId);
        return Ok(new { status = "emitted", correlationId = decisionRequest.CorrelationId });
    }

    /// <summary>
    /// Emit decision made receipt
    /// </summary>
    /// <param name="decisionMade">Decision made data</param>
    /// <returns>Acknowledgment</returns>
    [HttpPost("decision-made")]
    public IActionResult EmitDecisionMade([FromBody] DecisionMadeReceipt decisionMade)
    {
        if (decisionMade == null)
        {
            return BadRequest("Decision made data is required");
        }

        _logger.LogInformation("Decision made receipt emitted: {CorrelationId}", decisionMade.CorrelationId);
        return Ok(new { status = "emitted", correlationId = decisionMade.CorrelationId });
    }
}

/// <summary>
/// Decision requested receipt payload
/// </summary>
public class DecisionRequestedReceipt
{
    /// <summary>
    /// Unique correlation ID for tracking
    /// </summary>
    public string CorrelationId { get; set; }

    /// <summary>
    /// Actor type (human/agent)
    /// </summary>
    public string ActorType { get; set; }

    /// <summary>
    /// Actor identity
    /// </summary>
    public string ActorIdentity { get; set; }

    /// <summary>
    /// Timestamp of request
    /// </summary>
    public DateTime Timestamp { get; set; }

    /// <summary>
    /// Source channel/message/thread IDs
    /// </summary>
    public string SourceChannel { get; set; }

    /// <summary>
    /// Decision payload (options, recommendation)
    /// </summary>
    public object DecisionPayload { get; set; }
}

/// <summary>
/// Decision made receipt payload
/// </summary>
public class DecisionMadeReceipt
{
    /// <summary>
    /// Unique correlation ID for tracking
    /// </summary>
    public string CorrelationId { get; set; }

    /// <summary>
    /// Actor type (human/agent)
    /// </summary>
    public string ActorType { get; set; }

    /// <summary>
    /// Actor identity
    /// </summary>
    public string ActorIdentity { get; set; }

    /// <summary>
    /// Timestamp of decision
    /// </summary>
    public DateTime Timestamp { get; set; }

    /// <summary>
    /// Source channel/message/thread IDs
    /// </summary>
    public string SourceChannel { get; set; }

    /// <summary>
    /// Selected option from decision payload
    /// </summary>
    public string SelectedOption { get; set; }

    /// <summary>
    /// Original decision payload
    /// </summary>
    public object OriginalPayload { get; set; }
}