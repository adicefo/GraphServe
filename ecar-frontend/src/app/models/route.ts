import { Client } from "./client";
import { Driver } from "./driver";

export interface Route{
    rid?:string;
    source_point_lat?:number;
    source_point_lon?:number;
    destination_point_lat?:number;
    destination_point_lon?:number;
    start_date?:Date;
    end_date?:Date;
    duration?:number;
    number_of_kilometers?:number;
    full_price?:number;
    paid?:boolean;
    status?:string;
    client?:Client;
    driver?:Driver;
}