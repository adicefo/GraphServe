import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { GooglePlacePrediction, GooglePlaceDetails } from '../models/route';

@Injectable({
    providedIn: 'root'
})
export class GoogleMapsService {
    private isLoadedSubject = new BehaviorSubject<boolean>(false);
    public isLoaded$ = this.isLoadedSubject.asObservable();

    private autocompleteService: google.maps.places.AutocompleteService | null = null;
    private geocoder: google.maps.Geocoder | null = null;
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
            this.geocoder = new window.google.maps.Geocoder();
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
   async getAddressLatLng(lat: number, lng: number): Promise<string> {
  return new Promise((resolve, reject) => {
    const geocoder = new google.maps.Geocoder();
    const latlng = { lat, lng };

    geocoder.geocode({ location: latlng }, (results: any, status: any) => {
      if (status === 'OK' && results.length > 0) {
        let address = '';

        for (const result of results) {
          const components = result.address_components;

          const city =
            components.find((c: any) => c.types.includes('locality'))?.long_name ||
            components.find((c: any) => c.types.includes('administrative_area_level_2'))?.long_name;

          const country = components.find((c: any) => c.types.includes('country'))?.long_name;

          const street = components.find((c: any) => c.types.includes('route'))?.long_name;
          const number = components.find((c: any) => c.types.includes('street_number'))?.long_name;

          if (city || street) {
            address = '';
            if (street && number) address += `${street} ${number}`;
            else if (street) address += street;

            if (city) {
              if (address) address += ', ';
              address += city;
            }

            if (country) {
              if (address) address += ', ';
              address += country;
            }

            if (address) break; // stop at first proper address
          }
        }

        // fallback if no readable address found
        if (!address) {
          address = results[0].formatted_address || 'Unknown location';
        }

        resolve(address);
      } else {
        reject('No address found');
      }
    });
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
