import { Injectable } from '@angular/core';
import {
  HttpEvent,
  HttpHandlerFn,
  HttpInterceptorFn,
  HttpRequest
} from '@angular/common/http';
import { Observable } from 'rxjs';

export const AuthInterceptor: HttpInterceptorFn = (req, next) => {
  const username = localStorage.getItem('username');
  const password = localStorage.getItem('password');

  if (username && password) {
    const authHeader = 'Basic ' + btoa(username + ':' + password);
    const cloned = req.clone({
      setHeaders: { Authorization: authHeader }
    });
    return next(cloned);
  }

  return next(req);
};
