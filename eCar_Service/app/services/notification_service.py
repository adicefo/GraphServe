from app.models.requests import RouteInsertRequest,VehicleInsertRequest,RentInsertRequest,ReviewInsertRequest,NotificationInsertRequest
from app.models.responses import RouteDTO,ClientDTO,DriverDTO,UserDTO,VehicleDTO,RentDTO,ReviewDTO,NotificationDTO
from app.models.domain import Client,Vehicle,Rent,User,Review,Driver,Route,Notification
from datetime import datetime
import uuid
from fastapi import HTTPException
from automapper import mapper

class NotificationService:
    def create_notification(self,request:NotificationInsertRequest):
         nid = str(uuid.uuid4())


         notification_node = Notification(
            nid=nid,
            title=request.title,
            content=request.content,
            image=request.image,
            adding_date=datetime.now(),
            for_client=request.for_client
        ).save()
         
         notification_dto = mapper.to(NotificationDTO).map(notification_node.__properties__)

         return notification_dto
        
       

        

        

        

