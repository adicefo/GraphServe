from neomodel import db
from app.models.domain import Route, Client, Driver,Vehicle  
from app.models.requests import RouteInsertRequest,VehicleInsertRequest
from app.models.responses import RouteDTO,ClientDTO,DriverDTO,UserDTO,VehicleDTO,ResultPage
from datetime import datetime
import uuid
from fastapi import HTTPException
from automapper import mapper

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