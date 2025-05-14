from datetime import datetime
import uuid
from app.models.domain import User, Client
from app.models.responses import UserDTO, ClientDTO
from app.models.requests import UserInsertRequest
from app import config
from neomodel import db
from automapper import mapper

class ClientService:
    def create_client(self, request: UserInsertRequest):
        if request.password != request.passwordConfirm:
            raise ValueError("Passwords do not match")
        user_uid = str(uuid.uuid4())
        user_node = User(
            uid=user_uid,
            name=request.name,
            surname=request.surname,
            username=request.username,
            email=request.email,
            telephoneNumber=request.telephoneNumber,
            gender=request.gender,
            active=request.isActive,
            registrationDate=datetime.now()
        ).save()
        
        client_uid=str(uuid.uuid4())
        client_node = Client(
            cid=client_uid
        ).save()

        client_node.user.connect(user_node)

        user_dto = mapper.to(UserDTO).map(user_node)

        client_dto = mapper.to(ClientDTO).map(client_node,fields_mapping={
            "user_id":user_node.uid,
            "user":user_dto
        })

        return client_dto
