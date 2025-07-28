from app.models.requests import RouteInsertRequest,VehicleInsertRequest,RentInsertRequest,ReviewInsertRequest,NotificationInsertRequest
from app.models.responses import RouteDTO,ClientDTO,DriverDTO,UserDTO,VehicleDTO,RentDTO,ReviewDTO,NotificationDTO,ResultPage
from app.models.domain import Client,Vehicle,Rent,User,Review,Driver,Route,Notification
from datetime import datetime
import uuid
from fastapi import HTTPException,status
from automapper import mapper
from neomodel.exceptions import *

class NotificationService:
    def get_notification_by_id(self, nid: str) -> NotificationDTO:
        try:
            notification: Notification = Notification.nodes.get(nid=nid)
        except (DoesNotExist, MultipleNodesReturned):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Notification with id '{nid}' not found",
            )

        

        notification_dto = mapper.to(NotificationDTO).map(
            notification)

        return notification_dto 
    def get_all_notifications(self):
         notifications:list[NotificationDTO]=[]

         for n in Notification.nodes.all():
              notification_dto=mapper.to(NotificationDTO).map(n)
              notifications.append(notification_dto)

         response=ResultPage[NotificationDTO]
         response.count=len(Notification.nodes)
         response.result=notifications
         return response
    
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
    
     
    def delete_notification(self,nid:str)->NotificationDTO:
          try:
            notification:Notification=Notification.nodes.get(nid=nid)
          except (DoesNotExist, MultipleNodesReturned):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Notification with id '{nid}' not found",
            )
         
          notification_dto=mapper.to(NotificationDTO).map(
              notification,
          )

          notification.delete()
          return notification_dto
         
         
         
       

        

        

        

