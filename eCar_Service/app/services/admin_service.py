from datetime import datetime
import uuid
from app.models.domain import Admin,User
from app.models.responses import AdminDTO,UserDTO
from app.models.requests import UserInsertRequest
from app import config
from neomodel import db
from automapper import mapper

class AdminService:
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