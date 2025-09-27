import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseService } from './base.service';
import { Route, CreateRouteRequest } from '../models/route';
import { Observable } from 'rxjs';



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

    /**
     * Update route status to active
     * @param id - Route ID
     * @param data - Update data
     * @returns Observable of API response
     */
    update(id: string, data: any): Observable<Route> {
        const url = `${this.baseUrl}/${this.endpoint}/${id}`;
        return this.http.put<Route>(url, data);
    }

    /**
     * Update route status to finished
     * @param id - Route ID
     * @returns Observable of API response
     */
    updateFinish(id: string): Observable<Route> {
        const url = `${this.baseUrl}/${this.endpoint}/${id}/finish`;
        return this.http.put<Route>(url, {});
    }

 
}