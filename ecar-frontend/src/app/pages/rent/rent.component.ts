import { Component, OnInit, OnDestroy, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MasterComponent } from '../master/master.component';
import { RentService } from '../../services/rent.service';
import { VehicleService } from '../../services/vehicle.service';
import { ClientService } from '../../services/client.service';
import { Rent,CreateRentRequest } from '../../models/rent';
import { Vehicle } from '../../models/vehicle';
import { Client } from '../../models/client';
import { Subscription, forkJoin } from 'rxjs';

@Component({
  selector: 'app-rent',
  standalone: true,
  imports: [CommonModule, FormsModule, MasterComponent],
  templateUrl: './rent.component.html',
  styleUrl: './rent.component.css',
  encapsulation: ViewEncapsulation.None
})
export class RentComponent implements OnInit, OnDestroy {
  rents: any[] = [];
  vehicles: Vehicle[] = [];
  clients: Client[] = [];
  loading = false;
  showAddModal = false;
  errors: any = {};

  formData = {
    rent_date: '',
    end_date: '',
    vehicle_id: '',
    client_id: '',
    status: ''
  };

  private subscriptions: Subscription[] = [];

  constructor(
    private rentService: RentService,
    private vehicleService: VehicleService,
    private clientService: ClientService
  ) {}

  ngOnInit(): void {
    this.loadData();
  }

  ngOnDestroy(): void {
    this.subscriptions.forEach(sub => sub.unsubscribe());
  }

  private loadData(): void {
    this.loading = true;
    const rentsRequest = this.rentService.getAll();
    const vehiclesRequest = this.vehicleService.getAll();
    const clientsRequest = this.clientService.getAll();

    const dataSubscription = forkJoin([rentsRequest, vehiclesRequest, clientsRequest])
      .subscribe({
        next: ([rentsResponse, vehiclesResponse, clientsResponse]) => {
          this.rents = rentsResponse.result || [];
          this.vehicles = vehiclesResponse.result || [];
          this.clients = clientsResponse.result || [];
          this.loading = false;
        },
        error: (error) => {
          console.error('Error loading data:', error);
          this.loading = false;
        }
      });

    this.subscriptions.push(dataSubscription);
  }

  openAddModal(): void {
    this.showAddModal = true;
    this.resetForm();
  }

  closeAddModal(): void {
    this.showAddModal = false;
    this.resetForm();
  }

  private resetForm(): void {
    this.formData = {
      rent_date: '',
      end_date: '',
      vehicle_id: '',
      client_id: '',
      status: ''
    };
    this.errors = {};
  }

  validateForm(): boolean {
    this.errors = {};
    if (!this.formData.rent_date) this.errors.rent_date = 'Rent date is required';
    if (!this.formData.end_date) this.errors.end_date = 'End date is required';
    if (!this.formData.vehicle_id) this.errors.vehicle_id = 'Vehicle is required';
    if (!this.formData.client_id) this.errors.client_id = 'Client is required';
    return Object.keys(this.errors).length === 0;
  }

  saveRent(): void {
    console.log("test validation");
    if (!this.validateForm()) return;
    console.log("passed validation");
    this.loading = true;
     const rentDateISO = this.formData.rent_date
    ? new Date(this.formData.rent_date + 'T00:00:00Z').toISOString()
    : '';
  const endDateISO = this.formData.end_date
    ? new Date(this.formData.end_date + 'T00:00:00Z').toISOString()
    :'';
    const rentData:CreateRentRequest={
      rent_date: rentDateISO,
      end_date: endDateISO,
      vehicle_id: this.formData.vehicle_id,
      client_id: this.formData.client_id,
    };
    console.log(rentData);
    const saveSubscription = this.rentService.createRent(rentData).subscribe({
      next: (res) => {
        this.loading = false;
        console.log('Rent created successfully');
        this.closeAddModal();
        this.loadData();
      },
      error: (error) => {
        console.error('Error creating rent:', error);
        this.loading = false;
      }
    });
    this.subscriptions.push(saveSubscription);
  }

  getVehicleName(rent: Rent): string {
    return rent.vehicle?.name || 'N/A';
  }

  getClientName(rent: Rent): string {
    if (rent.client && rent.client.user) {
      const user = rent.client.user;
      return `${user.name || ''} ${user.surname || ''}`.trim() || 'N/A';
    }
    return 'N/A';
  }

  getStatusBadgeClass(status?: string): string {
    switch (status) {
      case 'active': return 'badge bg-primary';
      case 'finished': return 'badge bg-success';
      case 'pending': return 'badge bg-warning';
      default: return 'badge bg-secondary';
    }
  }
}