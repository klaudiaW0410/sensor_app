from ninja import Schema
from typing import Optional


class SensorIn(Schema):
    name: str
    model: str
    description: Optional[str] = None


class SensorOut(Schema):
    id: int
    name: str
    model: str
    description: Optional[str] = None


class ReadingIn(Schema):
    temperature: float
    humidity: float
    timestamp: str


class ReadingOut(Schema):
    id: int
    sensor_id: int
    temperature: float
    humidity: float
    timestamp: str


class RegisterIn(Schema):
    username: str
    email: str
    password: str


class LoginIn(Schema):
    email: str
    password: str


class AuthOut(Schema):
    token: str
    user: dict


class ErrorOut(Schema):
    detail: str
