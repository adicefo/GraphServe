import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseService } from './base.service';
import { Review } from '../models/review';



@Injectable({
    providedIn: 'root'
})
export class ReviewService extends BaseService<Review> {
    constructor(http: HttpClient) {
        super(
            http,
            'http://localhost:8000',
            { endpoint: 'review' }
        );
    }
}