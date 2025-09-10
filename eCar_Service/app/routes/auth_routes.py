from fastapi import APIRouter, Depends
from app.security.security import authenticate
from app.models.responses import UserDTO

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(user=Depends(authenticate)):
     return {"username": user.username, "uid": user.uid, "email": user.email}
