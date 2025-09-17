import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseService } from './base.service';
import { Notification } from '../models/notification';



@Injectable({
    providedIn: 'root'
})
export class NotificationService extends BaseService<Notification> {
    constructor(http: HttpClient) {
        super(
            http,
            'http://localhost:8000',
            { endpoint: 'notification' }
        );
    }
}