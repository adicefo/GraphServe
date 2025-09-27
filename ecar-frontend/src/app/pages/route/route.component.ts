import { Component, OnInit, OnDestroy, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MasterComponent } from '../master/master.component';
import { RouteService } from '../../services/route.service';
import { ClientService } from '../../services/client.service';
import { DriverService } from '../../services/driver.service';
import { GoogleMapsService } from '../../services/google-maps.service';
import { Route, CreateRouteRequest, GooglePlacePrediction } from '../../models/route';
import { Client } from '../../models/client';
import { Driver } from '../../models/driver';
import { Subscription, forkJoin } from 'rxjs';

@Component({
  selector: 'app-route',
  imports: [CommonModule, FormsModule, MasterComponent],
  templateUrl: './route.component.html',
  styleUrl: './route.component.css',
  encapsulation: ViewEncapsulation.None
})
export class RouteComponent implements OnInit, OnDestroy {
  routes: Route[] = [];
  clients: Client[] = [];
  drivers: Driver[] = [];
  loading = false;
  showAddModal = false;
  errors: any = {};

  // Google Maps related
  googleMapsLoaded = false;
  sourcePredictions: GooglePlacePrediction[] = [];
  destPredictions: GooglePlacePrediction[] = [];
  showSourcePredictions = false;
  showDestPredictions = false;

  // Form data
  formData = {
    source_point_lat: 0,
    source_point_lon: 0,
    destination_point_lat: 0,
    destination_point_lon: 0,
    client_id: '',
    driver_id: '',
    sourceAddress: '',
    destinationAddress: ''
  };

  private subscriptions: Subscription[] = [];

  constructor(
    private routeService: RouteService,
    private clientService: ClientService,
    private driverService: DriverService,
    private googleMapsService: GoogleMapsService
  ) { }

  ngOnInit(): void {
    this.loadData();
    this.initializeGoogleMaps();
  }

  ngOnDestroy(): void {
    this.subscriptions.forEach(sub => sub.unsubscribe());
  }

  private initializeGoogleMaps(): void {
    const googleMapsSubscription = this.googleMapsService.isLoaded$.subscribe(
      (loaded) => {
        this.googleMapsLoaded = loaded;
      }
    );
    this.subscriptions.push(googleMapsSubscription);
  }

  private loadData(): void {
    this.loading = true;
    const routesRequest = this.routeService.getAll();
    const clientsRequest = this.clientService.getAll();
    const driversRequest = this.driverService.getAll();

    const dataSubscription = forkJoin([routesRequest, clientsRequest, driversRequest])
      .subscribe({
        next: ([routesResponse, clientsResponse, driversResponse]) => {
          this.routes = routesResponse.result || [];
          this.clients = clientsResponse.result || [];
          this.drivers = driversResponse.result || [];
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
      source_point_lat: 0,
      source_point_lon: 0,
      destination_point_lat: 0,
      destination_point_lon: 0,
      client_id: '',
      driver_id: '',
      sourceAddress: '',
      destinationAddress: ''
    };
    this.errors = {};
    this.sourcePredictions = [];
    this.destPredictions = [];
    this.showSourcePredictions = false;
    this.showDestPredictions = false;
  }

  async onSourceSearch(event: any): Promise<void> {
    const query = event.target.value;
    this.formData.sourceAddress = query;

    if (!this.googleMapsLoaded || query.length < 3) {
      this.sourcePredictions = [];
      this.showSourcePredictions = false;
      return;
    }

    try {
      this.sourcePredictions = await this.googleMapsService.searchPlaces(query);
      this.showSourcePredictions = this.sourcePredictions.length > 0;
    } catch (error) {
      console.error('Error searching places:', error);
      this.sourcePredictions = [];
      this.showSourcePredictions = false;
    }
  }

  async onDestSearch(event: any): Promise<void> {
    const query = event.target.value;
    this.formData.destinationAddress = query;

    if (!this.googleMapsLoaded || query.length < 3) {
      this.destPredictions = [];
      this.showDestPredictions = false;
      return;
    }

    try {
      this.destPredictions = await this.googleMapsService.searchPlaces(query);
      this.showDestPredictions = this.destPredictions.length > 0;
    } catch (error) {
      console.error('Error searching places:', error);
      this.destPredictions = [];
      this.showDestPredictions = false;
    }
  }

  async selectPlace(place: GooglePlacePrediction, isSource: boolean): Promise<void> {
    try {
      const coords = await this.googleMapsService.getPlaceDetails(place.place_id);

      if (isSource) {
        this.formData.sourceAddress = place.description;
        this.formData.source_point_lat = coords.latitude;
        this.formData.source_point_lon = coords.longitude;
        this.showSourcePredictions = false;
      } else {
        this.formData.destinationAddress = place.description;
        this.formData.destination_point_lat = coords.latitude;
        this.formData.destination_point_lon = coords.longitude;
        this.showDestPredictions = false;
      }
    } catch (error) {
      console.error('Error selecting place:', error);
    }
  }

  validateForm(): boolean {
    this.errors = {};

    if (!this.formData.client_id) {
      this.errors.client_id = 'Client is required';
    }

    if (!this.formData.driver_id) {
      this.errors.driver_id = 'Driver is required';
    }

    if (this.formData.source_point_lat === 0 || this.formData.source_point_lon === 0) {
      this.errors.source = 'Source location is required';
    }

    if (this.formData.destination_point_lat === 0 || this.formData.destination_point_lon === 0) {
      this.errors.destination = 'Destination location is required';
    }

    return Object.keys(this.errors).length === 0;
  }

  async saveRoute(): Promise<void> {
    if (!this.validateForm()) {
      return;
    }

    this.loading = true;

    const routeData: CreateRouteRequest = {
      source_point_lat: this.formData.source_point_lat,
      source_point_lon: this.formData.source_point_lon,
      destination_point_lat: this.formData.destination_point_lat,
      destination_point_lon: this.formData.destination_point_lon,
      client_id: this.formData.client_id,
      driver_id: this.formData.driver_id
    };

    const saveSubscription = this.routeService.create(routeData).subscribe({
      next: (response) => {
        console.log('Route created successfully');
        this.loading = false;
        this.closeAddModal();
        this.loadData(); // Reload the routes
      },
      error: (error) => {
        console.error('Error creating route:', error);
        this.loading = false;
      }
    });

    this.subscriptions.push(saveSubscription);
  }

  async activateRoute(route: Route): Promise<void> {
    if (!route.id) return;

    this.loading = true;
    const activateSubscription = this.routeService.update(route.id, {}).subscribe({
      next: (response) => {
        console.log('Route activated successfully');
        this.loading = false;
        this.loadData();
      },
      error: (error) => {
        console.error('Error activating route:', error);
        this.loading = false;
      }
    });

    this.subscriptions.push(activateSubscription);
  }

  async finishRoute(route: Route): Promise<void> {
    if (!route.id) return;

    this.loading = true;
    const finishSubscription = this.routeService.updateFinish(route.id).subscribe({
      next: (response) => {
        console.log('Route finished successfully');
        this.loading = false;
        this.loadData();
      },
      error: (error) => {
        console.error('Error finishing route:', error);
        this.loading = false;
      }
    });

    this.subscriptions.push(finishSubscription);
  }

  getClientName(clientId?: string): string {
    if (!clientId) return 'N/A';
    const client = this.clients.find(c => c.cid === clientId);
    return client && client.user ? `${client.user.name || ''} ${client.user.surname || ''}`.trim() : 'N/A';
  }

  getDriverName(driverId?: string): string {
    if (!driverId) return 'N/A';
    const driver = this.drivers.find(d => d.did === driverId);
    return driver && driver.user ? `${driver.user.name || ''} ${driver.user.surname || ''}`.trim() : 'N/A';
  }

  getStatusBadgeClass(status?: string): string {
    switch (status) {
      case 'wait': return 'badge bg-warning';
      case 'active': return 'badge bg-primary';
      case 'finished': return 'badge bg-success';
      default: return 'badge bg-secondary';
    }
  }
}
