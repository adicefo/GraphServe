import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseService } from './base.service';
import { Vehicle } from '../models/vehicle';



@Injectable({
    providedIn: 'root'
})
export class VehicleService extends BaseService<Vehicle> {
    constructor(http: HttpClient) {
        super(
            http,
            'http://localhost:8000',
            { endpoint: 'vehicle' }
        );
    }
}