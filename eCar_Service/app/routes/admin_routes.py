from fastapi import APIRouter, HTTPException, Depends
from app.models.requests import UserInsertRequest
from app.models.responses import *
from app.services.admin_service import AdminService
from typing import List

router = APIRouter(prefix="/admin", tags=["admin"])

def get_admin_service():
    return AdminService()

@router.get("/",response_model=ResultPage[AdminDTO])
def get_all(service:AdminService=Depends(get_admin_service)):
    return service.get_all_admins()

@router.post("/", response_model=AdminDTO)
def create_client(request: UserInsertRequest, service: AdminService = Depends(get_admin_service)):
    return service.create_admin(request)