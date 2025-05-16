from fastapi import APIRouter, HTTPException, Depends
from app.models.requests import RentInsertRequest
from app.models.responses import RentDTO
from app.services.rent_service import RentService

router = APIRouter(prefix="/rent", tags=["rent"])

def get_rent_service():
    return RentService()

@router.post("/", response_model=RentDTO)
def create_rent(request: RentInsertRequest, service: RentService = Depends(get_rent_service)):
    return service.create_rent(request)