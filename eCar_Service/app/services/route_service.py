from neomodel import db
from app.models.domain import Route, Client, Driver  
from app.models.requests import RouteInsertRequest 
from app.models.responses import RouteDTO,ClientDTO,DriverDTO,UserDTO
from datetime import datetime
import uuid
from fastapi import HTTPException
from automapper import mapper

class RouteService:
    def create_route(self,request: RouteInsertRequest):

        client = Client.nodes.get_or_none(cid=request.client_id)
        client_user = client.user.single()
        if not client_user:
            raise HTTPException(404, f"User for client ID '{request.client_id}' not found")
        
        driver = Driver.nodes.get_or_none(did=request.driver_id)
        driver_user = driver.user.single()
        if not driver_user:
            raise HTTPException(404, f"User for driver ID '{request.driver_id}' not found")

        client_dto = mapper.to(ClientDTO).map(client, fields_mapping={
                "user_id": client_user.uid,
                "user": mapper.to(UserDTO).map(client_user)
        })

        driver_dto = mapper.to(DriverDTO).map(driver, fields_mapping={
            "user_id": driver_user.uid,
            "user": mapper.to(UserDTO).map(driver_user)
        })

        rid=str(uuid.uuid4())

        route_node = Route(
            rid=rid,
            source_point_lat=request.source_point_lat,
            source_point_lon=request.source_point_lon,
            destination_point_lat=request.destination_point_lat,
            destination_point_lon=request.destination_point_lon,
            duration=0,
            paid=False,
            number_of_kilometers=0.0,
            full_price=0.0,
            status="wait",
).save()
       
        
    
        

        # Create relationships
        route_node.client.connect(client)
        route_node.driver.connect(driver)

        route_dto=mapper.to(RouteDTO).map(route_node,fields_mapping={
"client":client_dto,
"driver":driver_dto
        })

        return route_dto
