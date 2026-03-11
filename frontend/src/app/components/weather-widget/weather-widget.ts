import { Component, OnInit, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api.service';

declare var lucide: any;

@Component({
  selector: 'app-weather-widget',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './weather-widget.html',
  styleUrls: ['./weather-widget.css']
})
export class WeatherWidgetComponent implements OnInit, AfterViewInit {
  weatherData: any = null;

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.apiService.getWeather().subscribe({
      next: (data) => {
        this.weatherData = data;
        setTimeout(() => {
          if (typeof lucide !== 'undefined') {
            lucide.createIcons();
          }
        }, 100);
      },
      error: (err) => console.error('Weather API Error:', err)
    });
  }

  getIcon(condition: string): string {
    if (!condition) return 'cloud';
    const cond = condition.toLowerCase();
    if (cond.includes('sunny')) return 'sun';
    if (cond.includes('cloudy')) return 'cloud';
    if (cond.includes('rain')) return 'cloud-rain';
    if (cond.includes('storm')) return 'cloud-lightning';
    return 'cloud';
  }

  ngAfterViewInit() {
    setTimeout(() => {
      if (typeof lucide !== 'undefined') {
        lucide.createIcons();
      }
    }, 500);
  }
}
