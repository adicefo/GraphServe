import { Routes } from '@angular/router';
import { LoginComponent } from './pages/login/login.component';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { DriverComponent } from './pages/driver/driver.component';
import { ClientComponent } from './pages/client/client.component';
import { RouteComponent } from './pages/route/route.component';
import { NotificationComponent } from './pages/notification/notification.component';
import { StatisticsComponent } from './pages/statistics/statistics.component';
import { RentComponent } from './pages/rent/rent.component';
import { VehicleComponent } from './pages/vehicle/vehicle.component';
import { ReviewComponent } from './pages/review/review.component';
export const routes: Routes = [
    {path:'',component:LoginComponent},
    {path:'dashboard',component:DashboardComponent},
    {path:'drivers',component:DriverComponent},
    {path:'clients',component:ClientComponent},
    {path:'routes',component:RouteComponent},
    {path:'rents',component:RentComponent},
    {path:'vehicles',component:VehicleComponent},
    {path:'reviews',component:ReviewComponent},
    {path:'notifications',component:NotificationComponent},
    {path:'statistics',component:StatisticsComponent}

];
