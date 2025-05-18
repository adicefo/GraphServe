from math import*

EARTH_RADIUS_M = 6_376_500.0 

def haversine_distance_m(lat1: float, lon1: float,
                            lat2: float, lon2: float) -> float:
        
        φ1, λ1, φ2, λ2 = map(radians, (lat1, lon1, lat2, lon2))

        Δφ = φ2 - φ1
        Δλ = λ2 - λ1

        a = sin(Δφ / 2) ** 2 + cos(φ1) * cos(φ2) * sin(Δλ / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return EARTH_RADIUS_M * c