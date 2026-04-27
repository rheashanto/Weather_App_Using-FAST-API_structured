# ⛅ WeatherVault

A full-stack weather application built with **FastAPI**, **PostgreSQL**, and vanilla **HTML/JS**. Users can sign up, log in, search live weather for any city, save snapshots, and view their personal weather history.

---

## Features

- **Signup & Login** with JWT authentication
- **Live weather search** via OpenWeatherMap API
- **Save weather snapshots** per user
- **Personal saved weather history** — each user sees only their own data
- **Delete saved entries**
- **PostgreSQL** database with Alembic migrations

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python) |
| Database | PostgreSQL + SQLAlchemy 2.0 (async) |
| Migrations | Alembic |
| Auth | JWT (python-jose) + bcrypt (passlib) |
| Weather API | OpenWeatherMap |
| HTTP Client | httpx |
| Frontend | HTML + Vanilla JS |
| Package Manager | uv |

---

## Project Structure

```
weatherapp-backend/
└── fast_api/
    ├── fast_api/
    │   ├── db/
    │   │   ├── models/
    │   │   │   ├── user.py           # User table
    │   │   │   └── saved_weather.py  # SavedWeather table
    │   │   ├── migrations/           # Alembic migration files
    │   │   ├── base.py               # SQLAlchemy declarative base
    │   │   └── dependencies.py       # DB session injection
    │   ├── services/
    │   │   ├── auth.py               # Password hashing + JWT logic
    │   │   ├── weather.py            # OpenWeatherMap API integration
    │   │   └── dependencies.py       # get_current_user dependency
    │   ├── web/
    │   │   ├── api/
    │   │   │   ├── auth.py           # /auth/signup, /auth/login routes
    │   │   │   ├── weather.py        # /weather/* routes
    │   │   │   └── router.py         # Route registration
    │   │   ├── application.py        # FastAPI app factory
    │   │   └── lifespan.py           # DB startup/shutdown
    │   └── settings.py               # Config via pydantic-settings
    ├── .env                           # Environment variables (not committed)
    ├── alembic.ini                    # Alembic config
    └── pyproject.toml                 # Dependencies
frontend/
└── index.html                         # Single-page frontend app
```

---

## Database Schema

```sql
users (
  id           UUID PRIMARY KEY,
  email        VARCHAR(255) UNIQUE NOT NULL,
  username     VARCHAR(100) UNIQUE NOT NULL,
  hashed_password VARCHAR(255) NOT NULL,
  created_at   TIMESTAMPTZ DEFAULT now()
)

saved_weather (
  id           UUID PRIMARY KEY,
  user_id      UUID REFERENCES users(id) ON DELETE CASCADE,
  city         VARCHAR(100) NOT NULL,
  country      VARCHAR(10) NOT NULL,
  temperature  FLOAT NOT NULL,
  feels_like   FLOAT NOT NULL,
  humidity     INT NOT NULL,
  description  VARCHAR(255) NOT NULL,
  wind_speed   FLOAT NOT NULL,
  icon         VARCHAR(20) NOT NULL,
  saved_at     TIMESTAMPTZ DEFAULT now()
)
```

---

## Setup & Installation

### Prerequisites

- Python 3.12+
- PostgreSQL 14+
- [uv](https://docs.astral.sh/uv/) package manager
- OpenWeatherMap API key (free at https://openweathermap.org/api)

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd weatherapp-backend/fast_api
```

### 2. Install dependencies

```bash
uv sync
uv add "python-jose[cryptography]" "passlib[bcrypt]==1.7.4" httpx "bcrypt==4.0.1" "pydantic[email]"
```

### 3. Set up PostgreSQL

```bash
psql -U $(whoami) -d postgres
```

```sql
CREATE USER fast_api WITH PASSWORD 'fast_api';
CREATE DATABASE fast_api OWNER fast_api;
\q
```

### 4. Configure environment

Create a `.env` file in the `fast_api/` directory:

```env
FAST_API_RELOAD=True
FAST_API_HOST=127.0.0.1
FAST_API_PORT=8000

FAST_API_DB_HOST=localhost
FAST_API_DB_PORT=5432
FAST_API_DB_USER=fast_api
FAST_API_DB_PASS=fast_api
FAST_API_DB_BASE=fast_api

FAST_API_SECRET_KEY=your-long-random-secret-key
FAST_API_ACCESS_TOKEN_EXPIRE_MINUTES=30

FAST_API_OPENWEATHER_API_KEY=your_openweather_api_key
```

### 5. Run migrations

```bash
uv run alembic upgrade head
```

### 6. Start the backend

```bash
uv run python -m fast_api
```

API will be live at: http://127.0.0.1:8000  
Swagger docs at: http://127.0.0.1:8000/api/docs

### 7. Start the frontend

```bash
cd ../../frontend
python3 -m http.server 3000
```

Open http://localhost:3000 in your browser.

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/auth/signup` | No | Register a new user |
| POST | `/api/auth/login` | No | Login, returns JWT token |
| GET | `/api/weather/current?city=London` | Yes | Fetch live weather |
| POST | `/api/weather/save` | Yes | Save a weather snapshot |
| GET | `/api/weather/saved` | Yes | List your saved weather |
| DELETE | `/api/weather/saved/{id}` | Yes | Delete a saved entry |

### Authentication

All protected routes require a Bearer token in the header:

```
Authorization: Bearer <your_jwt_token>
```

Get the token from the signup or login response.

---

## How It Works

### Auth Flow
1. User signs up → password is hashed with bcrypt → stored in DB
2. Server returns a JWT token containing the user's ID
3. Client stores token in localStorage
4. Every protected request sends token in `Authorization` header
5. Server decodes token → fetches user → processes request

### Weather Flow
1. User searches a city → frontend sends GET request with JWT
2. Backend verifies token → calls OpenWeatherMap API
3. Weather data returned to frontend → user can save it
4. Save request → stored in `saved_weather` table linked to user ID
5. Saved list → queries only rows where `user_id = current_user.id`

---

## Known Issues / Notes

- New OpenWeatherMap API keys can take up to 2 hours to activate
- JWT tokens expire after 30 minutes (configurable in `.env`)
- `passlib` requires `bcrypt==4.0.1` — newer versions are incompatible
- Python 3.14 requires `asyncio.run()` instead of `get_event_loop()` in `env.py`

---

## Screenshots

| Page | Description |
|---|---|
| Login / Signup | Auth page with tab switching |
| Weather Search | Search any city, view live data |
| Saved Weather | Personal history with delete option |
