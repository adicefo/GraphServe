from app.models.requests import RouteInsertRequest,VehicleInsertRequest,RentInsertRequest,ReviewInsertRequest
from app.models.responses import RouteDTO,ClientDTO,DriverDTO,UserDTO,VehicleDTO,RentDTO,ResultPage,ReviewDTO
from app.models.domain import Client,Vehicle,Rent,User,Review,Driver,Route
from datetime import datetime
import uuid
from fastapi import HTTPException
from automapper import mapper
from neomodel import db

class ReviewService:
    @staticmethod
    def first_route_between(client_id: str, driver_id: str) -> Route | None:
        cypher = (
            "MATCH (c:Client {cid:$cid})<-[:OWNED_BY]-(r:Route)-[:DRIVEN_BY]->(:Driver {did:$did}) "
            "RETURN r LIMIT 1"
        )
        results, _ = db.cypher_query(cypher, {"cid": client_id, "did": driver_id})
        if results:
            # results[0][0] is the first row's first column (the Route node)
            return Route.inflate(results[0][0])
        return None
    
    def get_all_reviews(self):
        reviews_dto:list[ReviewDTO]=[]

        for review in Review.nodes.all():
            client=review.client.single()
            client_user=client.user.single()
            client_user_dto=mapper.to(UserDTO).map(client_user)

            client_dto=mapper.to(ClientDTO).map(
                client,
                fields_mapping={
                    "user_id":client_user.uid,
                    "user":client_user_dto
                }
            )

            driver=review.driver.single()
            driver_user=driver.user.single()
            driver_user_dto=mapper.to(UserDTO).map(driver_user)
            driver_dto=mapper.to(DriverDTO).map(
                driver,
                fields_mapping={
                    "user_id":driver_user.uid,
                    "user":driver_user_dto
                }
            )

            route=review.route.single()
            route_dto=mapper.to(RouteDTO).map(
                route,
                fields_mapping={
                    "client":client_dto,
                    "driver":driver_dto
                }
            )
            review_dto=mapper.to(ReviewDTO).map(
                review,
                fields_mapping={
                    "client":client_dto,
                    "driver":driver_dto,
                    "route":route_dto
                }
            )
            reviews_dto.append(review_dto)
        response=ResultPage[ReviewDTO]
        response.count=len(Review.nodes)
        response.result=reviews_dto
        return response
    

    def create_review(self,request:ReviewInsertRequest):
        client = Client.nodes.get_or_none(cid=request.reviews_id)
        client_user = client.user.single()
        if not client_user:
            raise HTTPException(404, f"User for client ID '{request.client_id}' not found")
        
        driver = Driver.nodes.get_or_none(did=request.reviewed_id)
        driver_user = driver.user.single()
        if not driver_user:
            raise HTTPException(404, f"User for driver ID '{request.driver_id}' not found")
        
        
        existing_route = self.first_route_between(request.reviews_id,request.reviewed_id)

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

        route_dto=mapper.to(RouteDTO).map(existing_route,fields_mapping={
            "client":client_dto,
            "driver":driver_dto
        })

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
    
    
