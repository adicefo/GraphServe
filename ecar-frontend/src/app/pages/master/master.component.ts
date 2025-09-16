import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-master',
  imports: [CommonModule],
  templateUrl: './master.component.html',
  styleUrl: './master.component.css'
})
export class MasterComponent {
 @Input() currentRoute: string = '';

  username: string="";
  currentDateTime: string ="";

  showInfo: boolean = false;

  constructor(private router: Router) {}
  ngOnInit() {
    this.username = localStorage.getItem('username') || 'User';

    this.updateDateTime();
    setInterval(() => this.updateDateTime(), 1000);

    

  }

  updateDateTime() {
    const now = new Date();
    this.currentDateTime = now.toLocaleString();
  }

  toggleInfo() {
    this.showInfo = !this.showInfo;
  }

  logout() {
    localStorage.removeItem('username');
    localStorage.removeItem('password');
    this.router.navigate(['']);
  }
  navigateToDashboard(){
    this.router.navigate(['dashboard']);
  }
}
