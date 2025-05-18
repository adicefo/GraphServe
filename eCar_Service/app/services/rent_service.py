from app.models.requests import RouteInsertRequest,VehicleInsertRequest,RentInsertRequest
from app.models.responses import RouteDTO,ClientDTO,DriverDTO,UserDTO,VehicleDTO,RentDTO,ResultPage
from app.models.domain import Client,Vehicle,Rent,User
from datetime import datetime
import uuid
from fastapi import HTTPException
from automapper import mapper

class RentService:
    def get_all_rents(self):
        rents_dto:list[RentDTO]=[]
        for rent in Rent.nodes.all():
            client=rent.client.single()
            client_user=client.user.single()
            client_user_dto = mapper.to(UserDTO).map(client_user)
            client_dto=mapper.to(ClientDTO).map(
                client,
                fields_mapping={
                    "user_id":client_user.uid,
                    "user":client_user_dto
                }
            )

            vehicle=rent.vehicle.single()
            vehicle_dto=mapper.to(VehicleDTO).map(vehicle)

            rent_dto=mapper.to(RentDTO).map(
                rent,
                fields_mapping={
                    "client":client_dto,
                    "vehicle":vehicle_dto
                }
            )
            rents_dto.append(rent_dto)
        response=ResultPage[RentDTO]
        response.count=len(Rent.nodes)
        response.result=rents_dto
        return response
    

    def create_rent(self,request:RentInsertRequest):
        client = Client.nodes.get_or_none(cid=request.client_id)
        client_user = client.user.single()
        if not client_user:
            raise HTTPException(404, f"User for client ID '{request.client_id}' not found")
        
        vehicle = Vehicle.nodes.get_or_none(vid=request.vehicle_id)
        if not vehicle:
            raise HTTPException(404, f"Vehicle with id '{request.vehicle_id}' not found")

        client_dto = mapper.to(ClientDTO).map(client, fields_mapping={
                "user_id": client_user.uid,
                "user": mapper.to(UserDTO).map(client_user)
        })

        vehicle_dto = mapper.to(VehicleDTO).map(vehicle)

        rid=str(uuid.uuid4())

        # Calculate number of days between rent_date and end_date
        number_of_days = (request.end_date - request.rent_date).days

        # Make sure it's at least 1 day (optional safety check)
        number_of_days = max(number_of_days, 1)

        # Calculate full price
        full_price = number_of_days * vehicle_dto.price

        # Create and save Rent node
        rent_node = Rent(
            rid=rid,
            rent_date=request.rent_date,
            end_date=request.end_date,
            number_of_days=number_of_days,
            paid=False,
            full_price=full_price,
            status="wait"
        ).save()

       
        
    
        

        # Create relationships
        rent_node.client.connect(client)
        rent_node.vehicle.connect(vehicle)

        rent_dto=mapper.to(RentDTO).map(rent_node,fields_mapping={
"client":client_dto,
"vehicle":vehicle_dto
        })

        return rent_dto
