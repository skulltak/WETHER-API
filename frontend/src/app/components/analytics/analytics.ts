import { Component, OnInit, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api.service';

declare var Chart: any;
declare var lucide: any;

@Component({
  selector: 'app-analytics',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './analytics.html',
  styleUrls: ['./analytics.css']
})
export class AnalyticsComponent implements OnInit, AfterViewInit {
  loadData: any = null;
  seasonalData: any = null;

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.apiService.getLoadPredictions().subscribe({
      next: (data) => {
        this.loadData = data;
        // Use timeout to ensure DOM is ready even if data comes fast
        setTimeout(() => this.initLoadChart(), 100);
      },
      error: (err) => console.error('Load Prediction Error:', err)
    });

    this.apiService.getSeasonalImpact().subscribe({
      next: (data) => {
        this.seasonalData = data;
        setTimeout(() => this.initSeasonalChart(), 100);
      },
      error: (err) => console.error('Seasonal Impact Error:', err)
    });
  }

  ngAfterViewInit() {
    if (typeof lucide !== 'undefined') {
      lucide.createIcons();
    }
  }

  private initLoadChart() {
    const canvas = document.getElementById('loadChart') as HTMLCanvasElement;
    if (typeof Chart === 'undefined' || !this.loadData || !canvas) {
      console.warn('Chart.js, data, or canvas missing for loadChart');
      return;
    }
    
    try {
      new Chart(canvas, {
        type: 'line',
        data: {
          labels: this.loadData.labels,
          datasets: [{
            label: 'ML PREDICTED LOAD',
            data: this.loadData.predictedLoad,
            borderColor: '#0ea5e9',
            backgroundColor: 'rgba(14, 165, 233, 0.05)',
            fill: true, tension: 0.4, borderWidth: 3, pointRadius: 2, pointBackgroundColor: '#fff'
          }, {
            label: 'BASELINE EXPECTED',
            data: this.loadData.baselineExpected,
            borderColor: '#64748b', borderDash: [5, 5], fill: false, tension: 0.4, borderWidth: 2
          }]
        },
        options: this.getCommonOptions()
      });
    } catch (e) {
      console.error('Error initializing loadChart:', e);
    }
  }

  private initSeasonalChart() {
    const canvas = document.getElementById('seasonalChart') as HTMLCanvasElement;
    if (typeof Chart === 'undefined' || !this.seasonalData || !canvas) {
      console.warn('Chart.js, data, or canvas missing for seasonalChart');
      return;
    }

    try {
      new Chart(canvas, {
        type: 'bar',
        data: {
          labels: this.seasonalData.labels,
          datasets: [{
            label: 'BASE LOAD',
            data: this.seasonalData.baseLoad,
            backgroundColor: '#0ea5e9', borderRadius: 4
          }, {
            label: 'FESTIVAL PEAK',
            data: this.seasonalData.festivalPeak,
            backgroundColor: '#f59e0b', borderRadius: 4
          }]
        },
        options: this.getCommonOptions()
      });
    } catch (e) {
      console.error('Error initializing seasonalChart:', e);
    }
  }

  private getCommonOptions() {
    return {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { 
          position: 'top', align: 'end', 
          labels: { usePointStyle: true, boxWidth: 8, padding: 20, color: '#334155', font: { weight: '600', size: 11 } } 
        }
      },
      scales: {
        y: { grid: { color: '#f1f5f9' }, border: { display: false }, ticks: { color: '#94a3b8', padding: 10 } },
        x: { grid: { display: false }, border: { display: false }, ticks: { color: '#94a3b8', padding: 10 } }
      }
    };
  }
}
