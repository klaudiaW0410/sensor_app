import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from sensors.models import Sensor




@pytest.mark.django_db
def test_register(client):
   response = client.post(
       "/api/auth/register/",
       data={
           "username": "testuser",
           "email": "test@test.com",
           "password": "password123"
       },
       content_type="application/json"
   )
   assert response.status_code == 201
   assert "token" in response.json()




@pytest.mark.django_db
def test_login(client):
   User.objects.create_user(username="testuser", email="test@test.com", password="password123")


   response = client.post(
       "/api/auth/token/",
       data={
           "email": "test@test.com",
           "password": "password123"
       },
       content_type="application/json"
   )
   assert response.status_code == 200
   assert "token" in response.json()




@pytest.mark.django_db
def test_create_sensor(client):
   user = User.objects.create_user("user", "u@test.com", "pass")
   token = Token.objects.create(user=user)


   response = client.post(
       "/api/sensors/",
       data={"name": "Sensor 1", "model": "DHT22", "description": "Test sensor"},
       content_type="application/json",
       HTTP_AUTHORIZATION=f"Bearer {token.key}"
   )
   assert response.status_code == 201
   assert response.json()["name"] == "Sensor 1"




@pytest.mark.django_db
def test_list_sensors(client):
   user = User.objects.create_user("user", "u@test.com", "pass")
   token = Token.objects.create(user=user)


   # utwórz jeden sensor
   Sensor.objects.create(owner=user, name="Sensor 1", model="DHT22", description="Desc")


   response = client.get(
       "/api/sensors/",
       HTTP_AUTHORIZATION=f"Bearer {token.key}"
   )
   assert response.status_code == 200
   assert len(response.json()) == 1




@pytest.mark.django_db
def test_create_reading(client):
   user = User.objects.create_user("user", "u@test.com", "pass")
   token = Token.objects.create(user=user)


   sensor = Sensor.objects.create(
       owner=user,
       name="Sensor",
       model="DHT22",
       description="Test sensor"
   )


   response = client.post(
       f"/api/sensors/{sensor.id}/readings/",
       data={
           "temperature": 22.5,
           "humidity": 40.0,
           "timestamp": "2026-01-05T10:00:00"
       },
       content_type="application/json",
       HTTP_AUTHORIZATION=f"Bearer {token.key}"
   )
   assert response.status_code == 201
   data = response.json()
   assert data["temperature"] == 22.5
   assert data["humidity"] == 40.0