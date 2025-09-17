import { Injectable, Inject, InjectionToken } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { BaseServiceConfig } from '../models/base.model';

export const API_BASE_URL = new InjectionToken<string>('API_BASE_URL');
export const SERVICE_CONFIG = new InjectionToken<BaseServiceConfig>('SERVICE_CONFIG');

@Injectable()
export class BaseService<T> {
    protected endpoint: string;
    protected customEndpoints = {
        getAll: '',
        getById: '/{id}',
        create: '',
        delete: '/{id}'
    };

    constructor(
        protected http: HttpClient,
        @Inject(API_BASE_URL) protected baseUrl: string,
        @Inject(SERVICE_CONFIG) config: BaseServiceConfig
    ) {
        this.endpoint = config.endpoint;
        if (config.customEndpoints) {
            this.customEndpoints = {
                ...this.customEndpoints,
                ...config.customEndpoints
            };
        }
    }

    /**
     * Get all items
     * @param params - Query parameters
     * @returns Observable of API response
     */
    getAll(params: any = {}): Observable<T[]> {
        // Filter out any null, undefined, or empty string values
        const filteredParams = this.filterParams(params);
        const url = `${this.baseUrl}/${this.endpoint}${this.customEndpoints.getAll}`;

        return this.http.get<T[]>(url, { params: filteredParams });
    }

    /**
     * Get a single item by ID
     * @param id - Item ID
     * @returns Observable of API response
     */
    getById(id: string | number): Observable<T> {
        const url = `${this.baseUrl}/${this.endpoint}${this.customEndpoints.getById.replace('{id}', id.toString())}`;
        return this.http.get<T>(url);
    }

    /**
     * Create a new item
     * @param data - Item data
     * @returns Observable of API response
     */
    create(data: T): Observable<T> {
        const url = `${this.baseUrl}/${this.endpoint}${this.customEndpoints.create}`;
        return this.http.post<T>(url, data);
    }

    /**
     * Save (create or update) an item
     * @param data - Item data
     * @returns Observable of API response
     */
    save(data: T): Observable<T> {
        return this.create(data);
    }



    /**
     * Delete an item
     * @param id - Item ID
     * @returns Observable of API response
     */
    delete(id: string | number): Observable<any> {
        const url = `${this.baseUrl}/${this.endpoint}${this.customEndpoints.delete.replace('{id}', id.toString())}`;
        return this.http.delete(url);
    }

    /**
     * Filter out null, undefined and empty string values from params
     */
    private filterParams(params: any): HttpParams {
        let httpParams = new HttpParams();

        if (params) {
            Object.keys(params).forEach(key => {
                if (params[key] !== null &&
                    params[key] !== undefined &&
                    params[key] !== '') {
                    httpParams = httpParams.append(key, params[key]);
                }
            });
        }

        return httpParams;
    }
}