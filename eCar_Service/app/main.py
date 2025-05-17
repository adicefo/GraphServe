from fastapi import FastAPI
from app.routes import client_routes,admin_routes,driver_routes,route_routes,vehicle_routes,rent_routes,review_routes,notification_routes
import app.models.domain
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to eCar FastAPI Service!"}

app.include_router(client_routes.router)
app.include_router(admin_routes.router)
app.include_router(driver_routes.router)
app.include_router(route_routes.router)
app.include_router(vehicle_routes.router)
app.include_router(rent_routes.router)
app.include_router(review_routes.router)
app.include_router(notification_routes.router)
