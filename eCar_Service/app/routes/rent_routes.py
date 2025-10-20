from fastapi import APIRouter, HTTPException, Depends
from app.models.requests import RentInsertRequest
from app.models.responses import RentDTO,ResultPage
from app.services.rent_service import RentService

router = APIRouter(prefix="/rent", tags=["rent"])

def get_rent_service():
    return RentService()
@router.get("/{rid}", response_model=RentDTO)
def get_route_by_id(rid: str,service:RentService=Depends(get_rent_service)):
    return service.get_rent_by_id(rid)
@router.get("/",response_model=ResultPage[RentDTO])
def get_all(service:RentService=Depends(get_rent_service)):
    return service.get_all_rents()

@router.post("/", response_model=RentDTO)
def create_rent(request: RentInsertRequest, service: RentService = Depends(get_rent_service)):
    return service.create_rent(request)
@router.put("/update-active/{rid}", response_model=bool)
def update_active(rid:str, service: RentService = Depends(get_rent_service)):
    return service.update_active(rid)
@router.put("/update-finish/{rid}", response_model=bool)
def update_active(rid:str, service: RentService = Depends(get_rent_service)):
    return service.update_finish(rid)
@router.delete("/{rid}",response_model=RentDTO)
def remove_rent(rid:str,service:RentService=Depends(get_rent_service)):
    return service.delete_rent(rid)