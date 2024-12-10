import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-admin-dashboard',
  templateUrl: './admin-dashboard.component.html',
})
export class AdminDashboardComponent implements OnInit {
  stats: any = {};
  newCode: string = '';

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.loadStats();
  }

  loadStats() {
    this.apiService.viewStats().subscribe((data) => {
      this.stats = data;
    });
  }

  generateCode() {
    this.apiService.generateDiscount({ discount_percentage: 10 }).subscribe((data) => {
      this.newCode = data.code;
    });
  }
}
