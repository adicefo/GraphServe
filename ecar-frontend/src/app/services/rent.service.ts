import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseService } from './base.service';
import { Rent } from '../models/rent';



@Injectable({
    providedIn: 'root'
})
export class RentService extends BaseService<Rent> {
    constructor(http: HttpClient) {
        super(
            http,
            'http://localhost:8000',
            { endpoint: 'rent' }
        );
    }
}