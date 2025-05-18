from neomodel import db
from app.models.domain import Route, Client, Driver,Vehicle  
from app.models.requests import RouteInsertRequest,VehicleInsertRequest
from app.models.responses import RouteDTO,ClientDTO,DriverDTO,UserDTO,VehicleDTO,ResultPage
from datetime import datetime
import uuid
from fastapi import HTTPException,status
from automapper import mapper
from neomodel.exceptions import *

class VehicleService:
    def get_all_vehicles(self):
        vehicles_dto:list[VehicleDTO]=[]

        for vehicle in Vehicle.nodes.all():
            vehicle_dto=mapper.to(VehicleDTO).map(vehicle)
            vehicles_dto.append(vehicle_dto)
        response=ResultPage[VehicleDTO]
        response.result=vehicles_dto
        response.count=len(Vehicle.nodes)
        return response
    
    def create_vehicle(self,request:VehicleInsertRequest):
        vehicle_vid=str(uuid.uuid4())

        vehicle_node=Vehicle(
            vid=vehicle_vid,
            name=request.name,
            price=request.price,
            average_fuel_consumption=request.average_fuel_consumption,
            available=request.available,
            image=request.image
        ).save()

        vehicle_dto=mapper.to(VehicleDTO).map(vehicle_node)

        return vehicle_dto
    def delete_vehicle(self,vid:str)->VehicleDTO:
        try:
            vehicle:Vehicle=Vehicle.nodes.get(vid=vid)
        except (DoesNotExist, MultipleNodesReturned):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vehicle with id '{vid}' not found",
            )
        vehicle_dto=mapper.to(VehicleDTO).map(
            vehicle
        )
        #first to delete all rents that are connected to this vehicle...
        cypher = """
        MATCH (v:Vehicle {vid: $vid})<-[:RENTED_VEHICLE]-(r:Rent)
        DETACH DELETE r
        """
        db.cypher_query(cypher, {"vid": vid})


        vehicle.delete()

        return vehicle_dto