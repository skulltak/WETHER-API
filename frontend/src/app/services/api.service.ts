import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, forkJoin } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:5283/api';

  constructor(private http: HttpClient) { }

  getWeather(lat: number = 19.0760, lon: number = 72.8777): Observable<any> {
    return this.http.get(`${this.apiUrl}/weather?lat=${lat}&lon=${lon}`);
  }

  getLoadPredictions(): Observable<any> {
    return this.http.get(`${this.apiUrl}/analytics/load`);
  }

  getSeasonalImpact(): Observable<any> {
    return this.http.get(`${this.apiUrl}/analytics/seasonal`);
  }

  getDashboardData(): Observable<any> {
    return forkJoin({
      weather: this.getWeather(),
      load: this.getLoadPredictions(),
      seasonal: this.getSeasonalImpact()
    });
  }
}
