from ninja import Router
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .schema import RegisterIn, LoginIn, AuthOut, ErrorOut

auth_router = Router()


@auth_router.post("/register/", response={201: AuthOut, 400: ErrorOut})
def register(request, payload: RegisterIn):
    if User.objects.filter(email=payload.email).exists():
        return 400, {"detail": "Email already exists"}
    
    if User.objects.filter(username=payload.username).exists():
        return 400, {"detail": "Username already exists"}
    
    user = User.objects.create_user(
        username=payload.username,
        email=payload.email,
        password=payload.password
    )
    
    token = Token.objects.create(user=user)  # <- DRF Token
    
    return 201, {
        "token": token.key,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }



@auth_router.post("/token/", response={200: AuthOut, 401: ErrorOut})
def login(request, payload: LoginIn):
    try:
        user = User.objects.get(email=payload.email)
    except User.DoesNotExist:
        return 401, {"detail": "Invalid credentials"}
    
    user = authenticate(username=user.username, password=payload.password)
    
    if user is None:
        return 401, {"detail": "Invalid credentials"}
    
    token, created = Token.objects.get_or_create(user=user)
    
    return 200, {
        "token": token.key,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }