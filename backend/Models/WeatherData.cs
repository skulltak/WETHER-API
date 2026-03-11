namespace backend.Models;

public class WeatherData
{
    public string City { get; set; } = string.Empty;
    public double Temperature { get; set; }
    public int RainProbability { get; set; }
    public string Condition { get; set; } = string.Empty;
    public List<ForecastDay> DailyForecast { get; set; } = new();
}

public class ForecastDay
{
    public DateTime Date { get; set; }
    public double MaxTemp { get; set; }
    public double MinTemp { get; set; }
    public int RainProbability { get; set; }
    public string Condition { get; set; } = string.Empty;
}
