import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseService, API_BASE_URL, SERVICE_CONFIG } from './base.service';
import { Driver } from '../models/driver';



@Injectable({
    providedIn: 'root'
})
export class DriverService extends BaseService<Driver> {
    constructor(http: HttpClient) {
        super(
            http,
            'http://localhost:8000', 
            { endpoint: 'driver' }
        );
    }
}