from neomodel import db
from app.models.domain import Route, Client, Driver  
from app.models.requests import RouteInsertRequest 
from app.models.responses import RouteDTO,ClientDTO,DriverDTO,UserDTO,ResultPage
from datetime import datetime
import uuid
from fastapi import HTTPException,status
from automapper import mapper
from neomodel.exceptions import *
from math import *
from app.utils.geo import  haversine_distance_m 

class RouteService:
             
    
  
    
    def get_all_routes(self):
        routes_dto: list[RouteDTO] = []

        for route in Route.nodes.all():  
            
            client = route.client.single()          
            client_user = client.user.single()      
            client_user_dto = mapper.to(UserDTO).map(client_user)
            client_dto = mapper.to(ClientDTO).map(
                client,
                fields_mapping={
                    "user_id": client_user.uid,
                    "user": client_user_dto,
                },
            )

           
            driver = route.driver.single()           
            driver_user = driver.user.single()       
            driver_user_dto = mapper.to(UserDTO).map(driver_user)
            driver_dto = mapper.to(DriverDTO).map(
                driver,
                fields_mapping={
                    "user_id": driver_user.uid,
                    "user": driver_user_dto,
                },
            )

            
            route_dto = mapper.to(RouteDTO).map(
                route,
                fields_mapping={
                    "client": client_dto,
                    "driver": driver_dto,
                },
            )
            routes_dto.append(route_dto)
        response=ResultPage[RouteDTO]
        response.result=routes_dto
        response.count=len(Route.nodes)
        return response

        
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

        #Calculates distance between lat and long
        distance_meters=haversine_distance_m(
            request.source_point_lat,request.source_point_lon,
            request.destination_point_lat,request.destination_point_lon
        )
        distance_kilometers=round(distance_meters/1000,3)
        full_price=distance_kilometers*3.07
        rid=str(uuid.uuid4())

        route_node = Route(
            rid=rid,
            source_point_lat=request.source_point_lat,
            source_point_lon=request.source_point_lon,
            destination_point_lat=request.destination_point_lat,
            destination_point_lon=request.destination_point_lon,
            duration=0,
            paid=False,
            number_of_kilometers=distance_kilometers,
            full_price=full_price,
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
    def delete_route(self,rid:str)->RouteDTO:
        
        try:
            route:Route=Route.nodes.get(rid=rid)
        except (DoesNotExist, MultipleNodesReturned):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Route with id '{rid}' not found",
            )
        client:Client=route.client.single()
        client_user=client.user.single()
        client_user_dto=mapper.to(UserDTO).map(client_user)
        client_dto=mapper.to(ClientDTO).map(
            client,
            fields_mapping={
                "user_id":client_user.uid,
                "user":client_user_dto
            }
        )

        driver:Driver=route.driver.single()
        driver_user=driver.user.single()
        driver_user_dto=mapper.to(UserDTO).map(driver_user)
        driver_dto=mapper.to(DriverDTO).map(
            driver,
            fields_mapping={
                "user_id":driver_user.uid,
                "user":driver_user_dto
            }
        )

        route_dto=mapper.to(RouteDTO).map(
            route,
            fields_mapping={
                "client":client_dto,
                "driver":driver_dto
            }
        )
          #first to delete all reviews that are connected to this vehicle...
        cypher = """
        MATCH (rr:Route {rid: $rid})<-[:REVIEWED_ROUTE]-(r:Review)
        DETACH DELETE r
        """
        db.cypher_query(cypher, {"rid": rid})

        route.delete()

        return route_dto
