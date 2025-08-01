from fastapi import APIRouter, HTTPException, Depends
from app.models.requests import RentInsertRequest,ReviewInsertRequest
from app.models.responses import ReviewDTO,ResultPage
from app.services.review_service import ReviewService

router = APIRouter(prefix="/review", tags=["review"])

def get_review_service():
    return ReviewService()
@router.get("/{rid}", response_model=ReviewDTO)
def get_route_by_id(rid: str,service:ReviewService=Depends(get_review_service)):
    return service.get_review_by_id(rid)
@router.get("/",response_model=ResultPage[ReviewDTO])
def get_all(service:ReviewService=Depends(get_review_service)):
    return service.get_all_reviews()

@router.post("/", response_model=ReviewDTO)
def create_rent(request: ReviewInsertRequest, service: ReviewService = Depends(get_review_service)):
    return service.create_review(request)

@router.delete("/{rid}",response_model=ReviewDTO)
def remove_review(rid:str,service:ReviewService=Depends(get_review_service)):
    return service.delete_review(rid)