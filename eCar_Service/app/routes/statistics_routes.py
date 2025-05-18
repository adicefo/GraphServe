from fastapi import APIRouter, HTTPException, Depends
from app.models.requests import StatisticsInsertRequest
from app.models.responses import StatisticsDTO,ResultPage
from app.services.statistics_service import StatisticsService

router=APIRouter(prefix="/statistics",tags=["statistics"])

def get_statistics_service():
    return StatisticsService()

@router.get("/",response_model=ResultPage[StatisticsDTO])
def get_all(serivce:StatisticsService=Depends(get_statistics_service)):
    return serivce.get_all_statistics()
@router.post(path="/",response_model=StatisticsDTO)
def create_statistics(request:StatisticsInsertRequest,service:StatisticsService=Depends(get_statistics_service)):
    return service.create_statistics(request)