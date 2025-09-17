import { Driver } from "./driver";


export interface Statistics{
    sid?:string;
    number_of_hours?:number;
    number_of_clients?:number;
    price_amount?:number;
    beginning_of_work?:Date;
    end_of_work?:Date;
    driver?:Driver;
}