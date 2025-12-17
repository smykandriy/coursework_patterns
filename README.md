# Car Rental System (Variant 19) — v4 Scaffold

This repository bootstraps a full-stack course project for a car rental system. It provides Dockerized Django + DRF (JWT) and React + TypeScript (Vite) scaffolding with minimal health checks and routing placeholders.

## Tech Stack

- Backend: Django 5, DRF, SimpleJWT, Postgres, CORS headers
- Frontend: React 18 + TypeScript (Vite), React Router, React Hook Form, Axios, MUI
- Tooling: Ruff, Black, isort, Pytest; ESLint + Prettier

## Repository Structure

- `backend/app/core/` — Django project configuration and health endpoint
- `backend/app/apps/` — Placeholder Django apps (`users`, `cars`, `bookings`, `pricing`, `payments`, `reports`, `common`)
- `frontend/` — Vite React TypeScript app with routing skeleton
- `docs/patterns.md` — Design and architecture notes (skeleton)
- `docker-compose.yml` — Postgres, backend, and frontend services

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local frontend work)
- Python 3.12+ (for local backend work)

### Environment Variables

1. Backend:
   ```bash
   cp backend/.env.example backend/.env
   ```
   Adjust database credentials and allowed origins as needed.
2. Frontend:
   ```bash
   cp frontend/.env.example frontend/.env
   ```
   Set `VITE_API_URL` to point at the backend API (default `http://localhost:8000/api`).

### Running with Docker

```bash
docker-compose up --build
```

Services:
- **db**: Postgres (with persistent volume `db_data`)
- **backend**: Django app served via `runserver` on `http://localhost:8000`
- **frontend**: Vite dev server on `http://localhost:5173`

Health check: `GET http://localhost:8000/api/health/` returns `{"status": "ok"}`.

### Local Development (without Docker)

- Backend:
  ```bash
  cd backend
  python -m venv .venv && source .venv/bin/activate
  pip install -r requirements-dev.txt
  cd app
  python manage.py migrate
  python manage.py runserver
  ```
- Frontend:
  ```bash
  cd frontend
  npm install
  npm run dev -- --host --port 5173
  ```

### Quality and Testing

- Backend lint/format: `ruff check backend/app`, `black backend/app`, `isort backend/app`
- Backend tests: `cd backend/app && pytest`
- Frontend lint/format: `cd frontend && npm run lint` (Prettier config included)

### Seeding

Placeholder: seeding scripts will be added in a future milestone.

### Architecture Overview

- **Backend**: Django project (`core`) wires DRF + JWT authentication and CORS. Domain-specific apps live in `backend/app/apps/` and should keep business logic in dedicated service modules with thin views/serializers.
- **Frontend**: React Router-based navigation with placeholder pages (Login, Register, Cars, My Bookings, Admin). API interactions should be centralized in service modules using the shared Axios client (`src/api/client.ts`).
