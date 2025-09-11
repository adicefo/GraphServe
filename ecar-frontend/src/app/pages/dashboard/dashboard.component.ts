import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MasterComponent } from "../master/master.component";
import { AuthService } from '../../services/auth.service';import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-dashboard',
  imports: [CommonModule, MasterComponent],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css'],
})
export class DashboardComponent implements OnInit {


  entities = [
    {
      name: 'Drivers',
      icon: '👤',
      route: '/drivers',
      shortDesc: 'Manage drivers',
      description: 'Add, edit, and manage driver profiles, licenses, and assignments'
    },
    {
      name: 'Clients',
      icon: '🧑‍🤝‍🧑',
      route: '/clients',
      shortDesc: 'Client management',
      description: 'Handle customer accounts, bookings, and client relationships'
    },
    {
      name: 'Routes',
      icon: '🛣️',
      route: '/routes',
      shortDesc: 'Route planning',
      description: 'Create and optimize travel routes for efficient service delivery'
    },
    {
      name: 'Rents',
      icon: '📅',
      route: '/rents',
      shortDesc: 'Rental bookings',
      description: 'Manage rental reservations, schedules, and booking history'
    },
    {
      name: 'Vehicles',
      icon: '🚙',
      route: '/vehicles',
      shortDesc: 'Fleet management',
      description: 'Track vehicle status, maintenance, and fleet operations'
    },
    {
      name: 'Reviews',
      icon: '⭐',
      route: '/reviews',
      shortDesc: 'Customer feedback',
      description: 'Monitor customer reviews, ratings, and service feedback'
    },
    {
      name: 'Notifications',
      icon: '🔔',
      route: '/notifications',
      shortDesc: 'System alerts',
      description: 'View system notifications, alerts, and important updates'
    },
    {
      name: 'Statistics',
      icon: '📊',
      route: '/statistics',
      shortDesc: 'Analytics & reports',
      description: 'Access business analytics, reports, and performance metrics'
    }
  ];

  constructor(private router: Router,private authService:AuthService,private http:HttpClient) { }

  ngOnInit(): void {
    console.log("Prosla");
  }

  navigate(route: string) {
    this.router.navigate([route]);
  }
}
