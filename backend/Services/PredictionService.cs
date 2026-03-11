namespace backend.Services;

public class PredictionService
{
    public object GetLoadPredictions()
    {
        // Mocking ML result for volume impact per 10mm rain
        return new
        {
            Correlation = 0.88,
            Labels = new[] { "08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00" },
            PredictedLoad = new[] { 3000, 3200, 3500, 3800, 3600, 3300, 3100 },
            BaselineExpected = new[] { 2800, 3000, 3200, 3400, 3300, 3100, 2900 }
        };
    }

    public object GetSeasonalImpact()
    {
        return new
        {
            Labels = new[] { "JUN", "JUL", "AUG", "SEP", "OCT", "NOV" },
            BaseLoad = new[] { 4000, 5200, 4800, 3500, 2800, 3200 },
            FestivalPeak = new[] { 4200, 4800, 5500, 3200, 3100, 5800 }
        };
    }
}
