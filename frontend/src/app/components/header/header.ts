import { Component, OnInit, AfterViewInit } from '@angular/core';

declare var lucide: any;

@Component({
  selector: 'app-header',
  standalone: true,
  templateUrl: './header.html',
  styleUrls: ['./header.css']
})
export class HeaderComponent implements OnInit, AfterViewInit {
  currentDate: string = '';
  lastUpdated: string = 'SYNCING...';
  isSyncing: boolean = false;

  ngOnInit() {
    this.currentDate = new Date().toLocaleDateString('en-IN', { 
      weekday: 'long', 
      day: 'numeric', 
      month: 'long', 
      year: 'numeric' 
    });
  }

  ngAfterViewInit() {
    if (typeof lucide !== 'undefined') {
      lucide.createIcons();
    }
  }

  onRefresh() {
    this.isSyncing = true;
    setTimeout(() => {
      this.isSyncing = false;
      this.lastUpdated = 'LAST SYNC: ' + new Date().toLocaleTimeString();
    }, 1500);
  }
}
