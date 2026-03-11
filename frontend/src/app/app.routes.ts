import { Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard';
import { RadarComponent } from './components/radar/radar';
import { RegionalComponent } from './components/regional/regional';
import { LiveSearchComponent } from './components/live-search/live-search';
import { AnalyticsComponent } from './components/analytics/analytics';

export const routes: Routes = [
  { path: '', redirectTo: '/forecast', pathMatch: 'full' },
  { path: 'forecast', component: DashboardComponent },
  { path: 'radar', component: RadarComponent },
  { path: 'analytics', component: AnalyticsComponent },
  { path: 'regional', component: RegionalComponent },
  { path: 'search', component: LiveSearchComponent },
  { path: '**', redirectTo: '/forecast' }
];
