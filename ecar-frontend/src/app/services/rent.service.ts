import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseService } from './base.service';
import { CreateRentRequest, Rent } from '../models/rent';
import { Observable } from 'rxjs/internal/Observable';



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

     createRent(rent: CreateRentRequest): Observable<any> {
  return this.http.post('http://localhost:8000/rent/', rent);
}
}