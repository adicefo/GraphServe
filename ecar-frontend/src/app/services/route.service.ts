import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseService } from './base.service';
import { Route } from '../models/route';



@Injectable({
    providedIn: 'root'
})
export class RouteService extends BaseService<Route> {
    constructor(http: HttpClient) {
        super(
            http,
            'http://localhost:8000',
            { endpoint: 'route' }
        );
    }
}