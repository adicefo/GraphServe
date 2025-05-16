from fastapi import APIRouter, HTTPException, Depends
from app.models.requests import VehicleInsertRequest
from app.models.responses import VehicleDTO
from app.services.vehicle_service import VehicleService

router = APIRouter(prefix="/vehicle", tags=["vehicle"])

def get_vehicle_service():
    return VehicleService()

@router.post("/", response_model=VehicleDTO)
def create_route(request: VehicleInsertRequest, service: VehicleService = Depends(get_vehicle_service)):
    return service.create_vehicle(request)