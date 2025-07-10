from fastapi import APIRouter, HTTPException, Depends
from app.models.requests import UserInsertRequest
from app.models.responses import *
from app.services.driver_service import DriverService

router = APIRouter(prefix="/driver", tags=["driver"])

def get_driver_service():
    return DriverService()
@router.get("/{did}", response_model=DriverDTO)
def get_driver_by_id(did: str,service:DriverService=Depends(get_driver_service)):
    return service.get_driver_by_id(did)
@router.get("/",response_model=ResultPage[DriverDTO])
def get_all_drivers(service:DriverService=Depends(get_driver_service)):
    return service.get_all_drivers()

@router.post("/", response_model=DriverDTO)
def create_client(request: UserInsertRequest, service: DriverService = Depends(get_driver_service)):
    return service.create_driver(request)

@router.delete("/{did}", response_model=DriverDTO)
def remove_driver(did: str, service: DriverService = Depends(get_driver_service)):
    return service.delete_driver(did)