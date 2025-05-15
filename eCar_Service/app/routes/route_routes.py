from fastapi import APIRouter, HTTPException, Depends
from app.models.requests import RouteInsertRequest
from app.models.responses import RouteDTO
from app.services.route_service import RouteService

router = APIRouter(prefix="/route", tags=["route"])

def get_route_service():
    return RouteService()

@router.post("/", response_model=RouteDTO)
def create_route(request: RouteInsertRequest, service: RouteService = Depends(get_route_service)):
    return service.create_route(request)
