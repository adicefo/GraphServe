import { Client } from "./client";
import { Driver } from "./driver";
import { Route } from "./route";


export interface Review{
    rid?:string;
    value?:number;
    description?:string;
    adding_date?:Date;
    client?:Client;
    driver?:Driver;
    route?:Route;
}