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
     * Update route status to active
     * @param id - Route ID
     * @returns Observable of API response
     */
   updateActive(rid: string): Observable<boolean> {
  const url = `${this.baseUrl}/${this.endpoint}`+'/update-active/'+rid;
  console.log(url);
  return this.http.put<boolean>(url, {});
}

updateFinish(rid:string):Observable<boolean>{
    const url = `${this.baseUrl}/${this.endpoint}`+'/update-finish/'+rid;
    return this.http.put<boolean>(url,{});
}
 
}