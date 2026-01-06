# Sensor Management API

**Junior backend coding test : Django 5 + Django Ninja + PostgreSQL**

---

## Tech stack

- Python 3.11
- Django 5.2.9
- Django Ninja
- PostgreSQL
- Docker & docker-compose
- Authentication: Django Rest Framework TokenAuth
- Tests: pytest, pytest-django

---

## Run project (Docker)

### Requirements

- Docker
- Docker Compose

### Build & run containers
```bash
make up
```

or directly:
```bash
docker-compose up --build -d
```

### Check running containers
```bash
docker-compose ps
```

### API docs

- [http://localhost:8000/api/docs](http://localhost:8000/api/docs)

---
## Frontend Setup

npm i
npm run dev

## Database setup

### Run migrations
```bash
docker-compose exec web python manage.py migrate
```

### Seed initial data
While keeping terminal running with docker, open another terminal in new tab and do:
```bash
docker-compose exec web python manage.py seed
```

> Creates a `seed_user` (password `secret123`) and sample sensors/readings from CSV.

---

## Environment variables

Configured in `docker-compose.yml`:

- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`

---

## Authentication

Token-based authentication using `rest_framework.authtoken`.

### Register

**Endpoint:** `POST /api/auth/register/`

**Request body:**
```json
{
  "username": "user1",
  "email": "user1@test.com",
  "password": "password123"
}
```

### Login

**Endpoint:** `POST /api/auth/token/`

Returns a token. Use it in requests:
```
Authorization: Bearer <token>
```

---

## API Overview

All endpoints are prefixed with `/api`.

### Sensors (auth required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/sensors/` | List sensors (pagination + search) |
| `POST` | `/api/sensors/` | Create sensor |
| `GET` | `/api/sensors/{id}/` | Sensor detail |
| `PUT` | `/api/sensors/{id}/` | Update sensor |
| `DELETE` | `/api/sensors/{id}/` | Delete sensor (cascades readings) |

### Readings (auth required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/sensors/{sensor_id}/readings/` | List readings<br>Optional filters: `timestamp_from`, `timestamp_to` |
| `POST` | `/api/sensors/{sensor_id}/readings/` | Create reading |

---

## Notes

- Timestamps must be ISO-formatted: `2026-01-05T10:30:00`
- Test database is automatically created and destroyed by pytest
-  Naive datetime warnings may appear if `USE_TZ=True` they can be ignored