import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  username: string = '';
  password: string = '';
  isObscured: boolean = true;

  constructor(private http: HttpClient, private router: Router) {}

  toggleVisibility() {
    this.isObscured = !this.isObscured;
  }

  login() {
    if (!this.username || !this.password) {
      alert('Please enter both username and password.');
      return;
    }

  
    localStorage.setItem('username', this.username);
    localStorage.setItem('password', this.password);

    this.http.post('http://localhost:8000/auth/login', {})
      .subscribe({
        next: (response: any) => {
          console.log("Login successful:", response);
        },
        error: (err) => {
          console.error("Login error:", err);
          alert('Invalid login credentials.');
          localStorage.removeItem('username');
          localStorage.removeItem('password');
        }
      });
}
  
}
