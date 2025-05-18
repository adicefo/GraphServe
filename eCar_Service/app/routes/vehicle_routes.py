from fastapi import APIRouter, HTTPException, Depends
from app.models.requests import VehicleInsertRequest
from app.models.responses import VehicleDTO,ResultPage
from app.services.vehicle_service import VehicleService

router = APIRouter(prefix="/vehicle", tags=["vehicle"])

def get_vehicle_service():
    return VehicleService()

@router.get("/", response_model=ResultPage[VehicleDTO])
def get_all(service: VehicleService = Depends(get_vehicle_service)):
    return service.get_all_vehicles()

@router.post("/", response_model=VehicleDTO)
def create_route(request: VehicleInsertRequest, service: VehicleService = Depends(get_vehicle_service)):
    return service.create_vehicle(request)