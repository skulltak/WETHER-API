using Microsoft.AspNetCore.Mvc;
using backend.Services;

namespace backend.Controllers;

[ApiController]
[Route("api/[controller]")]
public class AnalyticsController : ControllerBase
{
    private readonly PredictionService _predictionService;

    public AnalyticsController(PredictionService predictionService)
    {
        _predictionService = predictionService;
    }

    [HttpGet("load")]
    public IActionResult GetLoad() => Ok(_predictionService.GetLoadPredictions());

    [HttpGet("seasonal")]
    public IActionResult GetSeasonal() => Ok(_predictionService.GetSeasonalImpact());
}
