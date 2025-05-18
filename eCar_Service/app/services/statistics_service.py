from app.models.requests import StatisticsInsertRequest
from app.models.responses import StatisticsDTO,DriverDTO,ResultPage,UserDTO
from app.models.domain import Statistics,Driver
from datetime import datetime
import uuid
from fastapi import HTTPException,status
from automapper import mapper
from neomodel.exceptions import *
class StatisticsService:

    def get_all_statistics(self):
        statistics_dto:list[StatisticsDTO]=[]

        for statistics in Statistics.nodes.all():
            driver=statistics.driver.single()
            driver_user=driver.user.single()
            driver_user_dto=mapper.to(UserDTO).map(driver_user)

            driver_dto=mapper.to(DriverDTO).map(
                driver,
                fields_mapping={
                    "user_id":driver_user.uid,
                    "user":driver_user_dto
                }
            )

            s_response=mapper.to(StatisticsDTO).map(
                statistics,
                fields_mapping={
                    "driver":driver_dto
                }
            )
            statistics_dto.append(s_response)
        response=ResultPage[StatisticsDTO]
        response.count=len(Statistics.nodes)
        response.result=statistics_dto
        return response

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
    
    def delete_statistics(self,sid:str)->StatisticsDTO:
        try:
            statistics:Statistics=Statistics.nodes.get(sid=sid)
        except (DoesNotExist, MultipleNodesReturned):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Statistics with id '{sid}' not found",
            )
        
        driver=statistics.driver.single()
        driver_user=driver.user.single()
        driver_user_dto=mapper.to(UserDTO).map(driver_user)

        driver_dto=mapper.to(DriverDTO).map(
            driver,
            fields_mapping={
                "user_id":driver_user.uid,
                "user":driver_user_dto
            }
        )

        statistics_dto=mapper.to(StatisticsDTO).map(
            statistics,
            fields_mapping={
                "driver":driver_dto
            }
        )

        statistics.delete()

        return statistics_dto
        