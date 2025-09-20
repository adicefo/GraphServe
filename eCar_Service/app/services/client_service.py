from datetime import datetime
import uuid
from app.models.domain import User, Client
from app.models.responses import UserDTO, ClientDTO,ResultPage
from app.models.requests import UserInsertRequest
from app.models.search_objects import ClientSearchObject
from app import config
from neomodel import db
from automapper import mapper
from fastapi import HTTPException,status
from neomodel.exceptions import *
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class ClientService:
 def get_client_by_id(self, cid: str) -> ClientDTO:
    try:
        client: Client = Client.nodes.get(cid=cid)
    except (DoesNotExist, MultipleNodesReturned):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client with id '{cid}' not found",
        )

    user: User | None = client.user.single()
    user_dto = mapper.to(UserDTO).map(user) if user else None

    client_dto = mapper.to(ClientDTO).map(
        client,
        fields_mapping={
            "user_id": user.uid if user else None,
            "user": user_dto,
        },
    )

    return client_dto
 def get_all_clients(self,search:ClientSearchObject) -> ResultPage[ClientDTO]:
        clients_dto: list[ClientDTO] = []

    
        name = search.name or ""
        surname = search.surname or ""

        query = """
    MATCH (c:Client)-[:IS]->(u:User)
    WHERE ($name = "" OR toLower(u.name) CONTAINS toLower($name))
      AND ($surname = "" OR toLower(u.surname) CONTAINS toLower($surname))
    RETURN c, u
    """

        results, meta = db.cypher_query(query, {
        "name": name,
        "surname": surname
    })

        for c, u in results:
            client = Client.inflate(c)
            user = User.inflate(u)

            user_dto = mapper.to(UserDTO).map(user)
            client_dto = mapper.to(ClientDTO).map(
                client,
                fields_mapping={"user_id": user.uid, "user": user_dto},
            )
            clients_dto.append(client_dto)

        response = ResultPage[ClientDTO]
        response.result = clients_dto
        response.count = len(clients_dto)
        return response
 def create_client(self, request: UserInsertRequest):
        if request.password != request.password_conifrm:
            raise ValueError("Passwords do not match")
        hashed_password = pwd_context.hash(request.password)
        
        user_uid = str(uuid.uuid4())
        user_node = User(
            uid=user_uid,
            name=request.name,
            surname=request.surname,
            username=request.username,
            email=request.email,
            password=hashed_password,
            telephone_number=request.telephone_number,
            gender=request.gender,
            active=request.active,
            registration_date=datetime.now()
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
 def delete_client(self, cid: str) -> ClientDTO:
   

        try:
            client: Client = Client.nodes.get(cid=cid)
        except (DoesNotExist, MultipleNodesReturned):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with id '{cid}' not found",
            )
     
        user: User | None = client.user.single()
        user_dto = mapper.to(UserDTO).map(user) if user else None

        client_dto = mapper.to(ClientDTO).map(
            client,
            fields_mapping={
                "user_id": user.uid if user else None,
                "user": user_dto,
            },
        )

       
        client.delete()            
        if user:
            user.delete()         

        return client_dto