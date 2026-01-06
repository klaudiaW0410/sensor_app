from ninja import Router
from ninja.security import HttpBearer
from django.shortcuts import get_object_or_404
from django.db.models import Q
from typing import List
from datetime import datetime
from rest_framework.authtoken.models import Token
from .models import Sensor, Reading
from .schema import SensorIn, SensorOut, ReadingIn, ReadingOut, ErrorOut


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            token_obj = Token.objects.get(key=token)
            return token_obj.user
        except Token.DoesNotExist:
            return None


auth = AuthBearer()
sensors_router = Router()


# SENSOR ENDPOINTS 

@sensors_router.get("/", auth=auth, response=List[SensorOut])
def list_sensors(request, page: int = 1, page_size: int = 10, q: str = None):
    """List sensors with pagination and search"""
    sensors = Sensor.objects.filter(owner=request.auth)
    
    if q:
        sensors = sensors.filter(Q(name__icontains=q) | Q(model__icontains=q))
    
    start = (page - 1) * page_size
    end = start + page_size
    
    return [
        {
            "id": s.id,
            "name": s.name,
            "model": s.model,
            "description": s.description
        }
        for s in sensors[start:end]
    ]


@sensors_router.post("/", auth=auth, response={201: SensorOut})
def create_sensor(request, payload: SensorIn):
    """Create new sensor"""
    sensor = Sensor.objects.create(
        owner=request.auth,
        name=payload.name,
        model=payload.model,
        description=payload.description
    )
    
    return 201, {
        "id": sensor.id,
        "name": sensor.name,
        "model": sensor.model,
        "description": sensor.description
    }


@sensors_router.get("/{sensor_id}/", auth=auth, response={200: SensorOut, 404: ErrorOut})
def get_sensor(request, sensor_id: int):
    """Get sensor by ID"""
    sensor = get_object_or_404(Sensor, id=sensor_id, owner=request.auth)
    
    return 200, {
        "id": sensor.id,
        "name": sensor.name,
        "model": sensor.model,
        "description": sensor.description
    }


@sensors_router.put("/{sensor_id}/", auth=auth, response={200: SensorOut, 404: ErrorOut})
def update_sensor(request, sensor_id: int, payload: SensorIn):
    """Update sensor"""
    sensor = get_object_or_404(Sensor, id=sensor_id, owner=request.auth)
    
    sensor.name = payload.name
    sensor.model = payload.model
    sensor.description = payload.description
    sensor.save()
    
    return 200, {
        "id": sensor.id,
        "name": sensor.name,
        "model": sensor.model,
        "description": sensor.description
    }


@sensors_router.delete("/{sensor_id}/", auth=auth, response={204: None, 404: ErrorOut})
def delete_sensor(request, sensor_id: int):
    """Delete sensor (cascades readings)"""
    sensor = get_object_or_404(Sensor, id=sensor_id, owner=request.auth)
    sensor.delete()
    return 204, None


# READING ENDPOINTS

@sensors_router.get("/{sensor_id}/readings/", auth=auth, response={200: List[ReadingOut], 404: ErrorOut})
def list_readings(request, sensor_id: int, timestamp_from: str = None, timestamp_to: str = None):
    """List readings for a sensor with optional date filters"""
    sensor = get_object_or_404(Sensor, id=sensor_id, owner=request.auth)
    
    readings = Reading.objects.filter(sensor=sensor)
    
    # date filters
    if timestamp_from:
        try:
            dt_from = datetime.fromisoformat(timestamp_from)
            readings = readings.filter(timestamp__gte=dt_from)
        except ValueError:
            pass
    
    if timestamp_to:
        try:
            dt_to = datetime.fromisoformat(timestamp_to)
            readings = readings.filter(timestamp__lte=dt_to)
        except ValueError:
            pass
    
    readings = readings.order_by('-timestamp')
    
    return 200, [
        {
            "id": r.id,
            "sensor_id": r.sensor_id,
            "temperature": r.temperature,
            "humidity": r.humidity,
            "timestamp": r.timestamp.isoformat()
        }
        for r in readings
    ]


@sensors_router.post("/{sensor_id}/readings/", auth=auth, response={201: ReadingOut, 404: ErrorOut, 400: ErrorOut})
def create_reading(request, sensor_id: int, payload: ReadingIn):
    """Create new reading for a sensor"""
    sensor = get_object_or_404(Sensor, id=sensor_id, owner=request.auth)
    
    # parse timestamp
    try:
        timestamp = datetime.fromisoformat(payload.timestamp)
    except ValueError:
        return 400, {"detail": "Invalid timestamp format. Use: 2026-01-05T10:30:00"}
    
    # check duplicate
    if Reading.objects.filter(sensor=sensor, timestamp=timestamp).exists():
        return 400, {"detail": "Reading with this timestamp already exists"}
    
    # create reading
    reading = Reading.objects.create(
        sensor=sensor,
        temperature=payload.temperature,
        humidity=payload.humidity,
        timestamp=timestamp
    )
    
    return 201, {
        "id": reading.id,
        "sensor_id": reading.sensor_id,
        "temperature": reading.temperature,
        "humidity": reading.humidity,
        "timestamp": reading.timestamp.isoformat()
    }