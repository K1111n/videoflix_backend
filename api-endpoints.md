# Videoflix API Endpoint Dokumentation

---

## Authentication

### Login und Registrierung

---

#### `POST /api/register/`

**Description:** Registriert einen neuen Benutzer im System.

**Permissions:** Keine erforderlich

**Rate Limit:** Kein Limit

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "confirmed_password": "securepassword"
}
```

**Success Response `201`:**
> Nach erfolgreicher Registrierung wird eine Aktivierungs-E-Mail versendet. Der Response inkl. dem Token hat keine Verwendung im Frontend, da hier mit HTTP-Only-Cookies gearbeitet wird.
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com"
  },
  "token": "activation_token"
}
```

**Status Codes:**
| Code | Beschreibung |
|------|-------------|
| 201 | Benutzer erfolgreich erstellt |

> **Info:** Konto bleibt inaktiv bis zur Aktivierung via E-Mail.

---

#### `GET /api/activate/<uidb64>/<token>/`

**Description:** Aktiviert das Benutzerkonto mithilfe des per E-Mail gesendeten Tokens.

**Permissions:** Keine erforderlich

**Rate Limit:** Kein Limit

**URL Parameter:**
| Name | Beschreibung |
|------|-------------|
| `uidb64` | Base64-codierte Benutzer-ID |
| `token` | Aktivierungstoken |

**Success Response `200`:**
```json
{
  "message": "Account successfully activated."
}
```

**Status Codes:**
| Code | Beschreibung |
|------|-------------|
| 200 | Account erfolgreich aktiviert |
| 400 | Aktivierung fehlgeschlagen |

---

#### `POST /api/login/`

**Description:** Authentifiziert den Benutzer und gibt JWT-Tokens zurück.

**Permissions:** Keine erforderlich

**Rate Limit:** Kein Limit

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Success Response `200`:**
> JWT-Tokens, Benutzerinformationen und Cookies werden gesetzt. Der Response hat keine Verwendung im Frontend, da hier mit HTTP-Only-Cookies gearbeitet wird.
```json
{
  "detail": "Login successful",
  "user": {
    "id": 1,
    "username": "user@example.com"
  }
}
```

**Status Codes:**
| Code | Beschreibung |
|------|-------------|
| 200 | Login erfolgreich |

> **Info:** Setzt HttpOnly-Cookies: `access_token` & `refresh_token`.
> - `access_token`: Dient zur Authentifizierung bei API-Anfragen.
> - `refresh_token`: Wird verwendet, um einen neuen Zugangstoken zu erhalten.

---

#### `POST /api/logout/`

**Description:** Meldet den Benutzer ab, indem der Refresh-Token ungültig gemacht wird.

**Permissions:** Refresh-Token-Cookie erforderlich

**Rate Limit:** Kein Limit

**Request Body:** Keiner

**Success Response `200`:**
```json
{
  "detail": "Logout successful! All tokens will be deleted. Refresh token is now invalid."
}
```

**Status Codes:**
| Code | Beschreibung |
|------|-------------|
| 200 | Logout erfolgreich |
| 400 | Refresh-Token fehlt |

> **Info:** Löscht die Cookies `access_token` und `refresh_token`. Der Refresh-Token wird auf eine Blacklist gesetzt.

---

#### `POST /api/token/refresh/`

**Description:** Gibt ein neues Zugangstoken aus, wenn der alte Access-Token abgelaufen ist.

**Permissions:** Refresh-Token-Cookie erforderlich

**Rate Limit:** Kein Limit

**Request Body:** Keiner

**Success Response `200`:**
> Der Token im Response hat keine Verwendung im Frontend, da hier mit HTTP-Only-Cookies gearbeitet wird.
```json
{
  "detail": "Token refreshed",
  "access": "new_access_token"
}
```

**Status Codes:**
| Code | Beschreibung |
|------|-------------|
| 200 | Access-Token wurde erneuert |
| 400 | Refresh-Token fehlt |
| 401 | Ungültiger Refresh-Token |

> **Info:** Setzt neuen `access_token`-Cookie. Der `refresh_token` muss im Cookie vorhanden und gültig sein.

---

#### `POST /api/password_reset/`

**Description:** Sendet einen Link zum Zurücksetzen des Passworts an die E-Mail des Benutzers.

**Permissions:** Keine Authentifizierung erforderlich

**Rate Limit:** Kein Limit

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Success Response `200`:**
```json
{
  "detail": "An email has been sent to reset your password."
}
```

**Status Codes:**
| Code | Beschreibung |
|------|-------------|
| 200 | Reset-E-Mail wurde versendet |

> **Info:** Nur möglich, wenn ein Benutzer mit dieser E-Mail existiert.

---

#### `POST /api/password_confirm/<uidb64>/<token>/`

**Description:** Bestätigt die Passwortänderung mit dem in der E-Mail enthaltenen Token.

**Permissions:** Keine Authentifizierung erforderlich

**Rate Limit:** Kein Limit

**URL Parameter:**
| Name | Beschreibung |
|------|-------------|
| `uidb64` | Base64-codierte Benutzer-ID |
| `token` | Token zur Passwort-Zurücksetzung |

**Request Body:**
```json
{
  "new_password": "newsecurepassword",
  "confirm_password": "newsecurepassword"
}
```

**Success Response `200`:**
```json
{
  "detail": "Your Password has been successfully reset."
}
```

**Status Codes:**
| Code | Beschreibung |
|------|-------------|
| 200 | Passwort erfolgreich geändert |

---

## Video

### Videoanzeige, Streaming und Segmentbereitstellung

---

#### `GET /api/video/`

**Description:** Gibt eine Liste aller verfügbaren Videos zurück.

**Permissions:** JWT-Authentifizierung erforderlich

**Rate Limit:** Kein Limit

**Request Body:** Keiner

**Success Response `200`:**
```json
[
  {
    "id": 1,
    "created_at": "2023-01-01T12:00:00Z",
    "title": "Movie Title",
    "description": "Movie Description",
    "thumbnail_url": "http://example.com/media/thumbnail/image.jpg",
    "category": "Drama"
  },
  {
    "id": 2,
    "created_at": "2023-01-02T12:00:00Z",
    "title": "Another Movie",
    "description": "Another Description",
    "thumbnail_url": "http://example.com/media/thumbnail/image2.jpg",
    "category": "Romance"
  }
]
```

**Status Codes:**
| Code | Beschreibung |
|------|-------------|
| 200 | Liste erfolgreich zurückgegeben |
| 401 | Nicht authentifiziert |
| 500 | Interner Serverfehler |

---

#### `GET /api/video/<movie_id>/<resolution>/index.m3u8`

**Description:** Gibt die HLS-Master-Playlist für einen bestimmten Film und eine gewählte Auflösung zurück.

**Permissions:** JWT-Authentifizierung erforderlich

**Rate Limit:** Kein Limit

**URL Parameter:**
| Name | Typ | Beschreibung |
|------|-----|-------------|
| `movie_id` | int | Die ID des Films |
| `resolution` | string | Gewünschte Auflösung (z.B. `480p`, `720p`, `1080p`) |

**Request Body:** Keiner

**Success Response `200`:**
> Content-Type: `application/vnd.apple.mpegurl` — Body enthält HLS-Manifestdatei im M3U8-Format.

**Status Codes:**
| Code | Beschreibung |
|------|-------------|
| 200 | Manifest erfolgreich geliefert |
| 404 | Video oder Manifest nicht gefunden |

---

#### `GET /api/video/<movie_id>/<resolution>/<segment>/`

**Description:** Gibt ein einzelnes HLS-Videosegment für einen bestimmten Film in gewählter Auflösung zurück.

**Permissions:** JWT-Authentifizierung erforderlich

**Rate Limit:** Kein Limit

**URL Parameter:**
| Name | Typ | Beschreibung |
|------|-----|-------------|
| `movie_id` | int | ID des Films |
| `resolution` | string | Gewünschte Auflösung (z.B. `480p`, `720p`, `1080p`) |
| `segment` | string | Dateiname des Segments (z.B. `000.ts`) |

**Request Body:** Keiner

**Success Response `200`:**
> Content-Type: `video/MP2T` — Body enthält binäre Videodaten.

**Status Codes:**
| Code | Beschreibung |
|------|-------------|
| 200 | Segment erfolgreich geliefert |
| 404 | Video oder Segment nicht gefunden |
