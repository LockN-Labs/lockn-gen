/// <summary>
/// Receipt endpoints with XML documentation
/// </summary>
[ApiController]
[Route("api/[controller]")]
[ProducesResponseType(Status500)]
public class ReceiptEndpoints : ControllerBase
{
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
}