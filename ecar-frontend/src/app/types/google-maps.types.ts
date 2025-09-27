declare global {
    interface Window {
        google: typeof google;
    }
}

declare namespace google {
    namespace maps {
        class Map {
            constructor(mapDiv: HTMLElement, opts?: MapOptions);
        }

        interface MapOptions {
            center?: LatLng | LatLngLiteral;
            zoom?: number;
        }

        class LatLng {
            constructor(lat: number, lng: number);
            lat(): number;
            lng(): number;
        }

        interface LatLngLiteral {
            lat: number;
            lng: number;
        }

        class Geocoder {
            geocode(
                request: GeocoderRequest,
                callback: (results: GeocoderResult[], status: GeocoderStatus) => void
            ): void;
        }

        interface GeocoderRequest {
            location?: LatLng | LatLngLiteral;
            placeId?: string;
            address?: string;
        }

        interface GeocoderResult {
            formatted_address: string;
            geometry: {
                location: LatLng;
            };
        }

        enum GeocoderStatus {
            OK = "OK",
            ZERO_RESULTS = "ZERO_RESULTS",
            OVER_QUERY_LIMIT = "OVER_QUERY_LIMIT",
            REQUEST_DENIED = "REQUEST_DENIED",
            INVALID_REQUEST = "INVALID_REQUEST",
            UNKNOWN_ERROR = "UNKNOWN_ERROR"
        }

        namespace places {
            class AutocompleteService {
                getPlacePredictions(
                    request: AutocompletionRequest,
                    callback: (predictions: QueryAutocompletePrediction[], status: PlacesServiceStatus) => void
                ): void;
            }

            class PlacesService {
                constructor(map: Map);
                getDetails(
                    request: PlaceDetailsRequest,
                    callback: (place: PlaceResult, status: PlacesServiceStatus) => void
                ): void;
            }

            interface AutocompletionRequest {
                input: string;
                types?: string[];
                componentRestrictions?: {
                    country?: string | string[];
                };
            }

            interface QueryAutocompletePrediction {
                place_id: string;
                description: string;
            }

            interface PlaceDetailsRequest {
                placeId: string;
                fields: string[];
            }

            interface PlaceResult {
                geometry?: {
                    location: LatLng;
                };
                formatted_address?: string;
            }

            enum PlacesServiceStatus {
                OK = "OK",
                ZERO_RESULTS = "ZERO_RESULTS",
                OVER_QUERY_LIMIT = "OVER_QUERY_LIMIT",
                REQUEST_DENIED = "REQUEST_DENIED",
                INVALID_REQUEST = "INVALID_REQUEST",
                NOT_FOUND = "NOT_FOUND",
                UNKNOWN_ERROR = "UNKNOWN_ERROR"
            }
        }
    }
}

export { google };
