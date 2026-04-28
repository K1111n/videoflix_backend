# Videoflix Backend

REST API Backend für die Videoflix-Streaming-Plattform. Gebaut mit Django, Django REST Framework, PostgreSQL, Redis und Django RQ.

## Features

- JWT-Authentifizierung via HttpOnly-Cookies
- Benutzerregistrierung mit E-Mail-Aktivierung
- Passwort-Reset per E-Mail
- HLS-Video-Streaming (480p, 720p, 1080p)
- Automatische HLS-Konvertierung und Thumbnail-Generierung per ffmpeg
- Hintergrundverarbeitung mit Django RQ und Redis
- PostgreSQL als Datenbank, Redis als Cache

## Voraussetzungen

- Docker & Docker Compose

## Setup

**1. Repository klonen**
```bash
git clone <repo-url>
cd videoflix_backend
```

**2. Umgebungsvariablen einrichten**

Mac/Linux:
```bash
cp .env.example .env
```
Windows:
```bash
copy .env.example .env
```
Anschließend `.env` mit deinen Werten befüllen (E-Mail-Zugangsdaten, Secret Key usw.).

**3. Starten**
```bash
docker compose up --build
```

Die API ist dann erreichbar unter: `http://localhost:8000`

## Services

| Service | Beschreibung |
|---------|-------------|
| `web` | Django-Anwendung |
| `worker` | RQ-Worker für Hintergrundaufgaben |
| `db` | PostgreSQL-Datenbank |
| `redis` | Redis für Cache und Job-Queue |

## API-Endpunkte

Eine vollständige Übersicht aller Endpunkte befindet sich in [api-endpoints.md](api-endpoints.md).

### Authentifizierung
| Methode | Endpunkt | Beschreibung |
|---------|----------|-------------|
| POST | `/api/register/` | Benutzer registrieren |
| GET | `/api/activate/<uidb64>/<token>/` | Account aktivieren |
| POST | `/api/login/` | Einloggen |
| POST | `/api/logout/` | Ausloggen |
| POST | `/api/token/refresh/` | Access-Token erneuern |
| POST | `/api/password_reset/` | Passwort-Reset anfordern |
| POST | `/api/password_confirm/<uidb64>/<token>/` | Neues Passwort setzen |

### Video
| Methode | Endpunkt | Beschreibung |
|---------|----------|-------------|
| GET | `/api/video/` | Alle Videos abrufen |
| GET | `/api/video/<id>/<resolution>/index.m3u8` | HLS-Playlist |
| GET | `/api/video/<id>/<resolution>/<segment>/` | HLS-Segment |

## Admin

Django Admin erreichbar unter `http://localhost:8000/admin/`

Superuser anlegen:
```bash
docker compose exec web python manage.py createsuperuser
```
