from fastapi import APIRouter, HTTPException, Depends
from app.models.requests import NotificationInsertRequest
from app.models.responses import NotificationDTO
from app.services.notification_service import NotificationService

router=APIRouter(prefix="/notification", tags= ["notification"])

def get_notification_service():
    return NotificationService()

@router.post(path="/",response_model=NotificationDTO)
def create_notification(request:NotificationInsertRequest,service:NotificationService=Depends(get_notification_service)):
    return service.create_notification(request)
