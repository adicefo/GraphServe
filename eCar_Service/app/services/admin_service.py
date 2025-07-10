from datetime import datetime
import uuid
from app.models.domain import Admin,User
from app.models.responses import AdminDTO,UserDTO,ResultPage
from app.models.requests import UserInsertRequest
from app import config
from neomodel import db
from automapper import mapper
from typing import List
from fastapi import HTTPException, status

from neomodel.exceptions import DoesNotExist, MultipleNodesReturned
class AdminService:
   def get_admin_by_id(self, aid: str) -> AdminDTO:
    try:
        admin: Admin = Admin.nodes.get(aid=aid)
    except (DoesNotExist, MultipleNodesReturned):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Admin with id '{aid}' not found",
        )

    user: User | None = admin.user.single()
    user_dto = mapper.to(UserDTO).map(user) if user else None

    admin_dto = mapper.to(AdminDTO).map(
        admin,
        fields_mapping={
            "user_id": user.uid if user else None,
            "user": user_dto,
        },
    )

    return admin_dto


   def get_all_admins(self) -> ResultPage[AdminDTO]:
        admins_dto: list[AdminDTO] = []

        for admin in Admin.nodes.all():          
            user = admin.user.single()          
            user_dto = mapper.to(UserDTO).map(user)

            admin_dto = mapper.to(AdminDTO).map(
                admin,
                fields_mapping={"user_id": user.uid, "user": user_dto},
            )
            admins_dto.append(admin_dto)
      
        response=ResultPage[AdminDTO]
        response.result=admins_dto
        response.count=len(Admin.nodes)

        
        return response
   def create_admin(self,request:UserInsertRequest):
        if request.password!=request.password_conifrm:
            raise ValueError("Password do not match")
        user_uid = str(uuid.uuid4())
        user_node = User(
            uid=user_uid,
            name=request.name,
            surname=request.surname,
            username=request.username,
            email=request.email,
            password=request.password,
            password_confirm=request.password_conifrm,
            telephone_number=request.telephone_number,
            gender=request.gender,
            active=request.active,
            registration_date=datetime.now()
        ).save()
        
        admin_uid=str(uuid.uuid4())
        admin_node = Admin(
            aid=admin_uid
        ).save()

        admin_node.user.connect(user_node)

        user_dto = mapper.to(UserDTO).map(user_node)

        admin_dto = mapper.to(AdminDTO).map(admin_node,fields_mapping={
            "user_id":user_node.uid,
            "user":user_dto
        })

        return admin_dto
   def delete_admin(self, aid: str) -> AdminDTO:
   
        try:
            admin: Admin = Admin.nodes.get(aid=aid)
        except (DoesNotExist, MultipleNodesReturned):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Admin with id '{aid}' not found",
            )
     
        user: User | None = admin.user.single()
        user_dto = mapper.to(UserDTO).map(user) if user else None

        admin_dto = mapper.to(AdminDTO).map(
            admin,
            fields_mapping={
                "user_id": user.uid if user else None,
                "user": user_dto,
            },
        )

       
        admin.delete()            
        if user:
            user.delete()         

        return admin_dto