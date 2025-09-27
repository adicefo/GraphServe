import { Client } from "./client";
import { Driver } from "./driver";

export interface Route {
    id?: string;
    source_point_lat?: number;
    source_point_lon?: number;
    destination_point_lat?: number;
    destination_point_lon?: number;
    start_date?: Date;
    end_date?: Date;
    duration?: number;
    number_of_kilometers?: number;
    full_price?: number;
    paid?: boolean;
    status?: string;
    client_id?: string;
    driver_id?: string;
    client?: Client;
    driver?: Driver;
}

export interface CreateRouteRequest {
    source_point_lat: number;
    source_point_lon: number;
    destination_point_lat: number;
    destination_point_lon: number;
    client_id: string;
    driver_id: string;
}

export interface GooglePlacePrediction {
    place_id: string;
    description: string;
}

export interface GooglePlaceDetails {
    latitude: number;
    longitude: number;
}