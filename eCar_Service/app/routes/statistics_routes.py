from fastapi import APIRouter, HTTPException, Depends
from app.models.requests import StatisticsInsertRequest
from app.models.responses import StatisticsDTO,ResultPage
from app.services.statistics_service import StatisticsService

router=APIRouter(prefix="/statistics",tags=["statistics"])

def get_statistics_service():
    return StatisticsService()
@router.get("/{sid}", response_model=StatisticsDTO)
def get_route_by_id(sid: str,service:StatisticsService=Depends(get_statistics_service)):
    return service.get_statistics_by_id(sid)
@router.get("/",response_model=ResultPage[StatisticsDTO])
def get_all(serivce:StatisticsService=Depends(get_statistics_service)):
    return serivce.get_all_statistics()
@router.post(path="/",response_model=StatisticsDTO)
def create_statistics(request:StatisticsInsertRequest,service:StatisticsService=Depends(get_statistics_service)):
    return service.create_statistics(request)
@router.delete("/{sid}",response_model=StatisticsDTO)
def remove_statistics(sid:str,service:StatisticsService=Depends(get_statistics_service)):
    return service.delete_statistics(sid)