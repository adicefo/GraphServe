import { User } from "./user";


export interface Client{
    cid?:string;
    user_id?:string;
    image?:string;
    user?:User;
}