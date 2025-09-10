import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MasterComponent } from "../master/master.component";

@Component({
  selector: 'app-dashboard',
  imports: [CommonModule, MasterComponent],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css'],
})
export class DashboardComponent implements OnInit {


  entities = [
    { name: 'Drivers', icon: '👤', route: '/drivers' },
    { name: 'Clients', icon: '🧑‍🤝‍🧑', route: '/clients' },
    { name: 'Routes', icon: '🛣️', route: '/routes' },
    { name: 'Rents', icon: '📅', route: '/rents' },
    { name: 'Vehicles', icon: '🚙', route: '/vehicles' },
    { name: 'Reviews', icon: '⭐', route: '/reviews' },
    { name: 'Notifications', icon: '🔔', route: '/notifications' },
    { name: 'Statistics', icon: '📊', route: '/statistics' }
  ];

  constructor(private router: Router) {}

   ngOnInit(): void {
       console.log("Prosla"); 
   }

  navigate(route: string) {
    this.router.navigate([route]);
  }
}
