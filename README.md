# Car Rental System (Variant 19)

Starter scaffolding for the Car Rental System course project (v4 milestone).

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Node.js 20+ (for local frontend development without Docker)
- Python 3.12+ (for local backend development without Docker)

### Environment Setup
- Copy `backend/.env.example` to `backend/.env` and adjust values as needed.
- Copy `frontend/.env.example` to `frontend/.env` and set `VITE_API_URL` for your backend.

### Running with Docker
```bash
docker-compose up --build
```
- Backend: http://localhost:8000/
- API base: http://localhost:8000/api/
- Health check: http://localhost:8000/api/health/
- Frontend dev server: http://localhost:5173/

### Running Locally (without Docker)
Backend:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app/manage.py migrate
python app/manage.py runserver
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

### Seeding
Seed data scripts will be added in a later milestone.

## Architecture Overview
- **Backend**: Django 5 + DRF + SimpleJWT, structured under `backend/app` with domain apps (`users`, `cars`, `bookings`, `pricing`, `payments`, `reports`, `common`). Settings pull configuration from environment variables and enable CORS and JWT authentication. A minimal `/api/health/` endpoint is available for sanity checks.
- **Frontend**: React + TypeScript (Vite) with React Router and Material UI. Routes for Login, Register, Cars, My Bookings, and Admin are scaffolded as placeholders. API access flows through a shared axios client using `VITE_API_URL`.
- **Docker**: `docker-compose.yml` orchestrates Postgres, backend, and frontend services with a shared database volume.
- **Quality Tooling**: Ruff/Black/Isort configurations for Python and ESLint/Prettier for the frontend; pytest scaffold for future backend tests.
