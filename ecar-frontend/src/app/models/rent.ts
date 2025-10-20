import { Client } from "./client";
import { Vehicle } from "./vehicle";


export interface Rent{
    rid?:string;
    rent_date?:Date;
    end_date?:Date;
    number_of_days?:number;
    full_price?:number;
    paid?:boolean;
    status?:string;
    vehicle?:Vehicle;
    client?:Client;
}

export interface CreateRentRequest {
    rent_date?: Date;
    end_date?: Date;
    vehicle_id?: String;
    client_id?: String;
}