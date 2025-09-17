from datetime import datetime
import uuid
from app.models.domain import Driver,User
from app.models.responses import DriverDTO,UserDTO,ResultPage
from app.models.requests import UserInsertRequest
from app.models.search_objects import DriverSearchObject
from app import config
from neomodel import db
from automapper import mapper
from fastapi import HTTPException,status
from neomodel.exceptions import *
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class DriverService:
 def get_driver_by_id(self, did: str) -> DriverDTO:
    try:
        driver: Driver = Driver.nodes.get(did=did)
    except (DoesNotExist, MultipleNodesReturned):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Driver with id '{did}' not found",
        )

    user: User | None = driver.user.single()
    user_dto = mapper.to(UserDTO).map(user) if user else None

    driver_dto = mapper.to(DriverDTO).map(
        driver,
        fields_mapping={
            "user_id": user.uid if user else None,
            "user": user_dto,
        },
    )

    return driver_dto
 def get_all_drivers(self, search: DriverSearchObject) -> ResultPage[DriverDTO]:
    drivers_dto: list[DriverDTO] = []

    
    name = search.name or ""
    surname = search.surname or ""

    query = """
    MATCH (d:Driver)-[:IS]->(u:User)
    WHERE ($name = "" OR toLower(u.name) CONTAINS toLower($name))
      AND ($surname = "" OR toLower(u.surname) CONTAINS toLower($surname))
    RETURN d, u
    """

    results, meta = db.cypher_query(query, {
        "name": name,
        "surname": surname
    })

    for d, u in results:
        driver = Driver.inflate(d)
        user = User.inflate(u)

        user_dto = mapper.to(UserDTO).map(user)
        driver_dto = mapper.to(DriverDTO).map(
            driver,
            fields_mapping={"user_id": user.uid, "user": user_dto},
        )
        drivers_dto.append(driver_dto)

    response = ResultPage[DriverDTO]
    response.result = drivers_dto
    response.count = len(drivers_dto)
    return response


    

 def create_driver(self,request:UserInsertRequest):
        if request.password!=request.password_conifrm:
            raise ValueError("Password do not match")
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
        
        driver_uid=str(uuid.uuid4())
        driver_node = Driver(
            did=driver_uid
        ).save()

        driver_node.user.connect(user_node)

        user_dto = mapper.to(UserDTO).map(user_node)

        driver_dto = mapper.to(DriverDTO).map(driver_node,fields_mapping={
            "user_id":user_node.uid,
            "user":user_dto
        })

        return driver_dto
 def delete_driver(self, did: str) -> DriverDTO:
   
        try:
            driver: Driver = Driver.nodes.get(did=did)
        except (DoesNotExist, MultipleNodesReturned):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Driver with id '{did}' not found",
            )
     
        user: User | None = driver.user.single()
        user_dto = mapper.to(UserDTO).map(user) if user else None

        driver_dto = mapper.to(DriverDTO).map(
            driver,
            fields_mapping={
                "user_id": user.uid if user else None,
                "user": user_dto,
            },
        )

       
        driver.delete()            
        if user:
            user.delete()         

        return driver_dto