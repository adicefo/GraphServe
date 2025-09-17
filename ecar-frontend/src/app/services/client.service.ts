import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseService } from './base.service';
import { Client } from '../models/client';



@Injectable({
    providedIn: 'root'
})
export class ClientService extends BaseService<Client> {
    constructor(http: HttpClient) {
        super(
            http,
            'http://localhost:8000',
            { endpoint: 'client' }
        );
    }
}