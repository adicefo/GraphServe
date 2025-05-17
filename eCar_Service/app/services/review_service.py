from app.models.requests import RouteInsertRequest,VehicleInsertRequest,RentInsertRequest,ReviewInsertRequest
from app.models.responses import RouteDTO,ClientDTO,DriverDTO,UserDTO,VehicleDTO,RentDTO,ReviewDTO
from app.models.domain import Client,Vehicle,Rent,User,Review,Driver,Route
from datetime import datetime
import uuid
from fastapi import HTTPException
from automapper import mapper

class ReviewService:
    def create_review(self,request:ReviewInsertRequest):
        client = Client.nodes.get_or_none(cid=request.reviews_id)
        client_user = client.user.single()
        if not client_user:
            raise HTTPException(404, f"User for client ID '{request.client_id}' not found")
        
        driver = Driver.nodes.get_or_none(did=request.reviewed_id)
        driver_user = driver.user.single()
        if not driver_user:
            raise HTTPException(404, f"User for driver ID '{request.driver_id}' not found")
        
        #TODO:Fix this error about finding the route
        existing_route = Route.nodes.filter(
            client_cid=request.reviews_id,   
            driver__did=request.reviewed_id   
        ).first()

        if not existing_route:
            raise HTTPException(
                404,
                f"No route found that involves client '{request.reviews_id}' and driver '{request.reviewed_id}'.")
        
        client_dto = mapper.to(ClientDTO).map(client, fields_mapping={
                "user_id": client_user.uid,
                "user": mapper.to(UserDTO).map(client_user)
        })

        driver_dto=mapper.to(DriverDTO).map(driver,fields_mapping={
              "user_id": driver_user.uid,
                "user": mapper.to(UserDTO).map(driver_user)
        })

        route_dto=mapper.to(RouteDTO).map(existing_route)

        rid=str(uuid.uuid4())

        review_node=Review(
            rid=rid,
            value=request.value,
            description=request.description,
            adding_date=datetime.now()
        ).save()

        review_node.client.connect(client)
        review_node.driver.connect(driver)
        review_node.route.connect(existing_route)

        review_dto=mapper.to(ReviewDTO).map(review_node,fields_mapping={
            "client":client_dto,
            "driver":driver_dto,
            "route":route_dto
        })
        return review_dto
