from fastapi import APIRouter, HTTPException, Depends
from app.models.requests import RouteInsertRequest
from app.models.responses import RouteDTO,ResultPage
from app.services.route_service import RouteService

router = APIRouter(prefix="/route", tags=["route"])

def get_route_service():
    return RouteService()

@router.get("/", response_model=ResultPage[RouteDTO])
def get_all_routes( service: RouteService = Depends(get_route_service)):
    return service.get_all_routes()
@router.post("/", response_model=RouteDTO)
def create_route(request: RouteInsertRequest, service: RouteService = Depends(get_route_service)):
    return service.create_route(request)

@router.delete("/{rid}",response_model=RouteDTO)
def remove_route(rid:str,service:RouteService=Depends(get_route_service)):
    return service.delete_route(rid)