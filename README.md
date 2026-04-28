# Videoflix Backend

REST API backend for the Videoflix streaming platform. Built with Django, Django REST Framework, PostgreSQL, Redis and Django RQ.

## Features

- JWT authentication via HttpOnly cookies
- User registration with email activation
- Password reset via email
- HLS video streaming (480p, 720p, 1080p)
- Automatic HLS conversion and thumbnail generation via ffmpeg
- Background processing with Django RQ and Redis
- PostgreSQL as database, Redis as cache

## Requirements

- Docker & Docker Compose

## Setup

**1. Clone the repository**
```bash
git clone <repo-url>
cd videoflix_backend
```

**2. Set up environment variables**

Mac/Linux:
```bash
cp .env.example .env
```
Windows:
```bash
copy .env.example .env
```
Fill in your values in `.env` (email credentials, secret key, etc.).

**3. Start**
```bash
docker compose up --build
```

The API will be available at: `http://localhost:8000`

## Services

| Service | Description |
|---------|-------------|
| `web` | Django application |
| `worker` | RQ worker for background tasks |
| `db` | PostgreSQL database |
| `redis` | Redis for cache and job queue |

## API Endpoints

A full overview of all endpoints can be found in [api-endpoints.md](api-endpoints.md).

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/register/` | Register a new user |
| GET | `/api/activate/<uidb64>/<token>/` | Activate account |
| POST | `/api/login/` | Log in |
| POST | `/api/logout/` | Log out |
| POST | `/api/token/refresh/` | Refresh access token |
| POST | `/api/password_reset/` | Request password reset |
| POST | `/api/password_confirm/<uidb64>/<token>/` | Set new password |

### Video
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/video/` | List all videos |
| GET | `/api/video/<id>/<resolution>/index.m3u8` | HLS playlist |
| GET | `/api/video/<id>/<resolution>/<segment>/` | HLS segment |

## Admin

Django Admin available at `http://localhost:8000/admin/`

Create a superuser:
```bash
docker compose exec web python manage.py createsuperuser
```
