using Microsoft.AspNetCore.Mvc;
using SinhalaEssayGrading.Models;

namespace SinhalaEssayGrading.Controllers;

[Route("api/[controller]")]
[ApiController]
public class EssayController: ControllerBase
{
    private readonly EssayGradingService _service;

    public EssayController(EssayGradingService service)
    {
        _service = service;
    }
    
    [HttpPost("grade")]
    public async Task<IActionResult> GradeEssay([FromBody] SinhalaEssayRequest request)
    {
        Console.WriteLine("Hello, World!");
        if (string.IsNullOrWhiteSpace(request.EssayText))
        {
            return BadRequest("Essay text cannot be empty.");
        }

        var result = await _service.GradeEssay(request.EssayText, request.ExpectedWordCount, request.Topic);
        return Ok(result);
    }
    
}