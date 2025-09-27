import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { GooglePlacePrediction, GooglePlaceDetails } from '../models/route';
import { google } from '../types/google-maps.types';

@Injectable({
    providedIn: 'root'
})
export class GoogleMapsService {
    private isLoadedSubject = new BehaviorSubject<boolean>(false);
    public isLoaded$ = this.isLoadedSubject.asObservable();

    private autocompleteService: google.maps.places.AutocompleteService | null = null;
    private geocoderService: google.maps.Geocoder | null = null;
    private placesService: google.maps.places.PlacesService | null = null;
    private map: google.maps.Map | null = null;

    constructor() {
        this.loadGoogleMaps();
    }

    /**
     * Load Google Maps API script
     */
    private loadGoogleMaps(): void {
        if (typeof window !== 'undefined') {
            if (window.google && window.google.maps) {
                this.initializeServices();
                return;
            }

            const script = document.createElement('script');
            script.src = `https://maps.googleapis.com/maps/api/js?key=${environment.googleMapsApiKey}&libraries=places`;
            script.async = true;
            script.defer = true;
            script.onload = () => {
                this.initializeServices();
            };
            script.onerror = (error) => {
                console.error('Error loading Google Maps API:', error);
            };
            document.head.appendChild(script);
        }
    }

    /**
     * Initialize Google Maps services
     */
    private initializeServices(): void {
        if (window.google && window.google.maps) {
            // Create a hidden map element for PlacesService
            const mapDiv = document.createElement('div');
            mapDiv.style.display = 'none';
            document.body.appendChild(mapDiv);

            this.map = new window.google.maps.Map(mapDiv, {
                center: { lat: 0, lng: 0 },
                zoom: 2,
            });

            this.autocompleteService = new window.google.maps.places.AutocompleteService();
            this.geocoderService = new window.google.maps.Geocoder();
            this.placesService = new window.google.maps.places.PlacesService(this.map);

            this.isLoadedSubject.next(true);
        }
    }

    /**
     * Check if Google Maps API is loaded
     */
    isLoaded(): boolean {
        return this.isLoadedSubject.value;
    }

    /**
     * Search for places using autocomplete
     */
    searchPlaces(query: string): Promise<GooglePlacePrediction[]> {
        return new Promise((resolve, reject) => {
            if (!this.autocompleteService || query.length < 3) {
                resolve([]);
                return;
            }

            this.autocompleteService.getPlacePredictions(
                { input: query },
                (predictions, status) => {
                    if (status === window.google.maps.places.PlacesServiceStatus.OK && predictions) {
                        const places = predictions.map((prediction) => ({
                            place_id: prediction.place_id,
                            description: prediction.description,
                        }));
                        resolve(places);
                    } else {
                        resolve([]);
                    }
                }
            );
        });
    }

    /**
     * Get place details including coordinates
     */
    getPlaceDetails(placeId: string): Promise<GooglePlaceDetails> {
        return new Promise((resolve, reject) => {
            if (!this.placesService) {
                reject('Places service not initialized');
                return;
            }

            this.placesService.getDetails(
                { placeId: placeId, fields: ['geometry'] },
                (place, status) => {
                    if (
                        status === window.google.maps.places.PlacesServiceStatus.OK &&
                        place &&
                        place.geometry &&
                        place.geometry.location
                    ) {
                        resolve({
                            latitude: place.geometry.location.lat(),
                            longitude: place.geometry.location.lng(),
                        });
                    } else {
                        reject('Place details not found');
                    }
                }
            );
        });
    }

    /**
     * Get address from latitude and longitude
     */
    getAddressFromLatLng(latitude: number, longitude: number): Promise<string> {
        return new Promise((resolve, reject) => {
            if (!this.geocoderService) {
                reject('Geocoder service not initialized');
                return;
            }

            this.geocoderService.geocode(
                {
                    location: { lat: parseFloat(latitude.toString()), lng: parseFloat(longitude.toString()) },
                },
                (results,status) => {
                    if (status === 'OK' && results && results.length > 0) {
                        resolve(results[0].formatted_address);
                    } else {
                        reject('Address not found');
                    }
                }
            );
        });
    }

    /**
     * Clean up resources
     */
    ngOnDestroy(): void {
        const mapDiv = document.querySelector('div[style*="display: none"]');
        if (mapDiv && mapDiv.parentNode) {
            document.body.removeChild(mapDiv);
        }
    }
}
