from fastapi import APIRouter, HTTPException, Depends
from app.models.requests import UserInsertRequest
from app.models.responses import ClientDTO
from app.services.client_service import ClientService

router = APIRouter(prefix="/client", tags=["client"])

def get_client_service():
    return ClientService()

@router.post("/", response_model=ClientDTO)
def create_client(request: UserInsertRequest, service: ClientService = Depends(get_client_service)):
    return service.create_client(request)
