from fastapi import FastAPI,HTTPException
from app import config 
from app.models.responses import *
from app.models.requests import *
from app.services.client_service import ClientService

app=FastAPI()

service=ClientService()

@app.get("/")
def read_root():
    return{"message":"Welcome to eCar FastAPI Service!"}

@app.post("/client/",response_model=ClientDTO)
def create_client(request:UserInsertRequest):
    return service.create_client(request)


