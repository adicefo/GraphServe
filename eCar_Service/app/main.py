from fastapi import FastAPI
from app.routes import client_routes,admin_routes,driver_routes

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to eCar FastAPI Service!"}

app.include_router(client_routes.router)
app.include_router(admin_routes.router)
app.include_router(driver_routes.router)
