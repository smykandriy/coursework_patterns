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
Seed demo data (users, cars, pricing rules, sample booking):
```bash
cd backend
python app/manage.py seed_demo
```

Demo credentials:
- Admin: `admin` / `adminpass`
- Manager: `manager` / `managerpass`
- Customer: `customer` / `customerpass`

## Architecture Overview
- **Backend**: Django 5 + DRF + SimpleJWT, structured under `backend/app` with domain apps (`users`, `cars`, `bookings`, `pricing`, `payments`, `reports`, `common`). Settings pull configuration from environment variables and enable CORS and JWT authentication. A minimal `/api/health/` endpoint is available for sanity checks.
- **Frontend**: React + TypeScript (Vite) with React Router and Material UI. Routes for Login, Register, Cars, My Bookings, and Admin are scaffolded as placeholders. API access flows through a shared axios client using `VITE_API_URL`.
- **Docker**: `docker-compose.yml` orchestrates Postgres, backend, and frontend services with a shared database volume.
- **Quality Tooling**: Ruff/Black/Isort configurations for Python and ESLint/Prettier for the frontend; pytest scaffold for future backend tests.

## API Endpoints (v2)
Base URL: `/api/`

| Area | Method | Path | Description |
| --- | --- | --- | --- |
| Auth | POST | `/auth/register/` | Register customer + profile |
| Auth | POST | `/auth/login/` | Obtain JWT (access + refresh) |
| Auth | POST | `/auth/refresh/` | Refresh JWT |
| Auth | GET/PATCH | `/auth/me/` | Get/update current user profile |
| Cars | GET | `/cars/` | List cars (filters + pagination) |
| Cars | GET | `/cars/{id}/` | Car detail |
| Cars | POST/PUT/PATCH/DELETE | `/cars/{id}/` | Admin/manager CRUD |
| Pricing | GET | `/pricing/quote?car=&start=&end=` | Pricing quote from service |
| Pricing | CRUD | `/pricing/rules/` | Pricing rules (admin only) |
| Bookings | GET/POST | `/bookings/` | Create/list bookings (customers see own) |
| Bookings | GET | `/bookings/{id}/` | Booking detail |
| Bookings | POST | `/bookings/{id}/confirm/` | Manager confirm |
| Bookings | POST | `/bookings/{id}/checkin/` | Manager check-in |
| Bookings | POST | `/bookings/{id}/return/` | Manager mark returned |
| Bookings | POST | `/bookings/{id}/cancel/` | Cancel booking |
| Bookings | GET/POST | `/bookings/{id}/fines/` | List/add fines (manager adds) |
| Payments | POST | `/bookings/{id}/deposit/hold|release|forfeit/` | Deposit actions |
| Payments | POST | `/bookings/{id}/invoice/pay/` | Pay invoice (mock) |
| Reports | ANY | `/reports/*` | Placeholder returns 501 |
| Schema | GET | `/schema/` | Basic OpenAPI schema |
