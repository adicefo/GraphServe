from fastapi import APIRouter, HTTPException, Depends
from fastapi.params import Query
from app.models.requests import UserInsertRequest
from app.models.responses import ClientDTO,ResultPage
from app.services.client_service import ClientService
from app.models.search_objects import *
router = APIRouter(prefix="/client", tags=["client"])

def get_client_service():
    return ClientService()
@router.get("/{cid}", response_model=ClientDTO)
def get_client_by_id(cid: str,service:ClientService=Depends(get_client_service)):
    return service.get_client_by_id(cid)
@router.get("/",response_model=ResultPage[ClientDTO])
def get_all_clients(
    name: Optional[str] = Query(None),
    surname: Optional[str] = Query(None),

    service: ClientService = Depends(get_client_service),
):
    search = ClientSearchObject(
        name=name,
        surname=surname,
    )
    return service.get_all_clients(search)

@router.post("/", response_model=ClientDTO)
def create_client(request: UserInsertRequest, service: ClientService = Depends(get_client_service)):
    return service.create_client(request)

@router.delete("/{cid}", response_model=ClientDTO)
def remove_client(cid: str, service: ClientService = Depends(get_client_service)):
    return service.delete_client(cid)