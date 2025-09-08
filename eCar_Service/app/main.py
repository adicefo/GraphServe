from fastapi import FastAPI, Depends
from app.security.security import authenticate
from app.routes import client_routes,admin_routes,driver_routes,route_routes,vehicle_routes,rent_routes,review_routes,notification_routes,statistics_routes
from fastapi.openapi.utils import get_openapi
app = FastAPI(dependencies=[Depends(authenticate)])

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
app.include_router(statistics_routes.router)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description="API with Basic Auth",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "basicAuth": {"type": "http", "scheme": "basic"}
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"basicAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi