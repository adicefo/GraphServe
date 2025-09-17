import { User } from "./user";
export interface Driver{
    did?:string;
    number_of_clients_amount?:number;
    number_of_hours_amount?:number;
    user_id?:string;
    user?:User;
}