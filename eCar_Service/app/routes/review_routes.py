from fastapi import APIRouter, HTTPException, Depends
from app.models.requests import RentInsertRequest,ReviewInsertRequest
from app.models.responses import ReviewDTO
from app.services.review_service import ReviewService

router = APIRouter(prefix="/review", tags=["review"])

def get_review_service():
    return ReviewService()

@router.get("/",response_model=list[ReviewDTO])
def get_all(service:ReviewService=Depends(get_review_service)):
    return service.get_all_reviews()

@router.post("/", response_model=ReviewDTO)
def create_rent(request: ReviewInsertRequest, service: ReviewService = Depends(get_review_service)):
    return service.create_review(request)