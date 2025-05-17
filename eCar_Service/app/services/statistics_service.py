from app.models.requests import StatisticsInsertRequest
from app.models.responses import StatisticsDTO,DriverDTO,UserDTO
from app.models.domain import Statistics,Driver
from datetime import datetime
import uuid
from fastapi import HTTPException
from automapper import mapper

class StatisticsService:
    def create_statistics(self,request:StatisticsInsertRequest):
        driver = Driver.nodes.get_or_none(did=request.driver_id)
        driver_user = driver.user.single()
        if not driver_user:
            raise HTTPException(404, f"User for driver ID '{request.driver_id}' not found")
        
        driver_dto=mapper.to(DriverDTO).map(driver,fields_mapping={
              "user_id": driver_user.uid,
                "user": mapper.to(UserDTO).map(driver_user)
        })

        statistics_node=Statistics(
            sid=str(uuid.uuid4()),
            number_of_hours=0,
            number_of_clients=0,
            price_amount=0.0,
            beginning_of_work=datetime.now()
        ).save()

        statistics_node.driver.connect(driver)

        statistics_dto=mapper.to(StatisticsDTO).map(statistics_node,fields_mapping=
                                                    {
                                                        "driver":driver_dto
                                                    })
        return statistics_dto