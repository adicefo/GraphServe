import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseService } from './base.service';
import { Statistics } from '../models/statistics';



@Injectable({
    providedIn: 'root'
})
export class StatisticsService extends BaseService<Statistics> {
    constructor(http: HttpClient) {
        super(
            http,
            'http://localhost:8000',
            { endpoint: 'statistics' }
        );
    }
}