from fastapi import APIRouter, HTTPException, Depends
from app.models.requests import NotificationInsertRequest
from app.models.responses import NotificationDTO,ResultPage
from app.services.notification_service import NotificationService

router=APIRouter(prefix="/notification", tags= ["notification"])

def get_notification_service():
    return NotificationService()
@router.get("/{nid}",response_model=NotificationDTO)
def get_route_by_id(nid: str,service:NotificationService=Depends(get_notification_service)):
    return service.get_notification_by_id(nid)
@router.get("/",response_model=ResultPage[NotificationDTO])
def get_all(service:NotificationService=Depends(get_notification_service)):
    return service.get_all_notifications()

@router.post(path="/",response_model=NotificationDTO)
def create_notification(request:NotificationInsertRequest,service:NotificationService=Depends(get_notification_service)):
    return service.create_notification(request)

@router.delete("/{nid}",response_model=NotificationDTO)
def remove_notification(nid:str,service:NotificationService=Depends(get_notification_service)):
    return service.delete_notification(nid)