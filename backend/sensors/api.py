from ninja import NinjaAPI
from .api_auth import auth_router
from .api_sensors import sensors_router

api = NinjaAPI(
    title="Sensor Management API",
    version="1.0.0"
)

# Add routers
api.add_router("/auth", auth_router, tags=["Authentication"])
api.add_router("/sensors", sensors_router, tags=["Sensors & Readings"])