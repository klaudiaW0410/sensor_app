# backend/sensors/api.py
from ninja import NinjaAPI

api = NinjaAPI()

@api.get("/hello")
def hello(request):
    """
    Minimalny test endpoint.
    ---
    returns: {"message": "Hello world!"}
    """
    return {"message": "Hello world!"}
