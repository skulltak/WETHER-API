using backend.Models;
using System.Text.Json;

namespace backend.Services;

public class WeatherService
{
    private readonly HttpClient _httpClient;

    public WeatherService(HttpClient httpClient)
    {
        _httpClient = httpClient;
    }

    public async Task<WeatherData> GetWeatherAsync(double lat, double lon)
    {
        // For accuracy, we use Open-Meteo with best_match models (incorporating ECMWF/GFS)
        var url = $"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=auto&models=best_match";
        
        var response = await _httpClient.GetAsync(url);
        response.EnsureSuccessStatusCode();
        
        var json = await response.Content.ReadAsStringAsync();
        using var document = JsonDocument.Parse(json);
        var root = document.RootElement;
        
        var current = root.GetProperty("current");
        var daily = root.GetProperty("daily");
        
        var data = new WeatherData
        {
            City = "Mumbai", // Hardcoded for now, or extracted from coordinates
            Temperature = current.GetProperty("temperature_2m").GetDouble(),
            RainProbability = daily.GetProperty("precipitation_probability_max")[0].GetInt32(),
            Condition = GetCondition(current.GetProperty("weather_code").GetInt32()),
            DailyForecast = new List<ForecastDay>()
        };

        var times = daily.GetProperty("time").EnumerateArray().ToList();
        var maxTemps = daily.GetProperty("temperature_2m_max").EnumerateArray().ToList();
        var minTemps = daily.GetProperty("temperature_2m_min").EnumerateArray().ToList();
        var rainProbs = daily.GetProperty("precipitation_probability_max").EnumerateArray().ToList();
        var codes = daily.GetProperty("weather_code").EnumerateArray().ToList();

        for (int i = 0; i < times.Count; i++)
        {
            data.DailyForecast.Add(new ForecastDay
            {
                Date = DateTime.Parse(times[i].GetString()!),
                MaxTemp = maxTemps[i].GetDouble(),
                MinTemp = minTemps[i].GetDouble(),
                RainProbability = rainProbs[i].GetInt32(),
                Condition = GetCondition(codes[i].GetInt32())
            });
        }

        return data;
    }

    private string GetCondition(int code)
    {
        if (code == 0) return "Sunny";
        if (code <= 3) return "Partly Cloudy";
        if (code >= 51 && code <= 67) return "Rainy";
        if (code >= 71) return "Stormy";
        return "Cloudy";
    }
}
