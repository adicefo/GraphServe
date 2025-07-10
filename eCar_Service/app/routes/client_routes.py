from fastapi import APIRouter, HTTPException, Depends
from app.models.requests import UserInsertRequest
from app.models.responses import ClientDTO,ResultPage
from app.services.client_service import ClientService

router = APIRouter(prefix="/client", tags=["client"])

def get_client_service():
    return ClientService()
@router.get("/{cid}", response_model=ClientDTO)
def get_client_by_id(cid: str,service:ClientService=Depends(get_client_service)):
    return service.get_client_by_id(cid)
@router.get("/",response_model=ResultPage[ClientDTO])
def get_all_clients(service:ClientService=Depends(get_client_service)):
    return service.get_all_clients()

@router.post("/", response_model=ClientDTO)
def create_client(request: UserInsertRequest, service: ClientService = Depends(get_client_service)):
    return service.create_client(request)

@router.delete("/{cid}", response_model=ClientDTO)
def remove_client(cid: str, service: ClientService = Depends(get_client_service)):
    return service.delete_client(cid)