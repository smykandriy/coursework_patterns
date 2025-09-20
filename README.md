# Car Rental System

Full-stack course project implementing a car rental workflow with Django REST Framework, PostgreSQL, and a React + Vite frontend. The system covers customer bookings, manager approvals, pricing strategies, deposit handling, and financial reports while demonstrating required GoF design patterns.

## Project structure

```
repo/
├─ backend/          # Django project & apps
├─ frontend/         # React + Vite SPA
├─ docker-compose.yml
└─ README.md
```

## Getting started with Docker

1. Copy environment examples:
   ```bash
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   ```
2. Build and start containers:
   ```bash
   docker-compose up --build
   ```
3. The API is available at `http://localhost:8000`, the frontend at `http://localhost:5173`.
4. Create demo data (optional but recommended):
   ```bash
   docker-compose run --rm backend python manage.py seed_demo
   ```

### Manual backend setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # adjust database credentials
python manage.py migrate
python manage.py runserver
```

Run tests with:
```bash
pytest
```

### Manual frontend setup

```bash
cd frontend
npm install
npm run dev
```

## Default demo credentials

| Role     | Email                 | Password    |
|----------|-----------------------|-------------|
| Admin    | `admin@example.com`   | `admin123`  |
| Manager  | `manager@example.com` | `manager123`|
| Customer | `customer@example.com`| `customer123`|

## API highlights

| Endpoint | Description |
|----------|-------------|
| `POST /api/auth/register/` | Register customer or staff users |
| `POST /api/auth/login/` | Obtain JWT tokens |
| `GET /api/cars/` | Browse cars with filters |
| `GET /api/pricing/quote/` | Retrieve quote using pricing strategy pipeline |
| `POST /api/bookings/` | Customer booking request |
| `POST /api/bookings/{id}/confirm/` | Manager confirmation, holds deposit |
| `POST /api/bookings/{id}/checkin/` | Start rental |
| `POST /api/bookings/{id}/return_car/` | Complete rental, calculates invoice & fines |
| `POST /api/bookings/{id}/cancel/` | Cancel booking (depending on state) |
| `POST /api/deposits/{booking_id}/{action}/` | Manual deposit hold/release/forfeit |
| `POST /api/invoices/{booking_id}/pay/` | Mock invoice payment |
| `GET /api/reports/*` | Fleet utilization & financial summaries |

Interactive OpenAPI docs: `http://localhost:8000/api/docs/`

## Implemented design patterns

| Pattern | Implementation |
|---------|----------------|
| Strategy | Pricing pipeline with `BasePriceStrategy`, `DurationDiscountStrategy`, `YearDepreciationStrategy`, `SeasonalStrategy` (`backend/app/apps/pricing/services.py`). |
| State | Booking life-cycle states (`PendingState`, `ConfirmedState`, `ActiveState`) in `backend/app/apps/bookings/services.py`. |
| Observer | Domain event bus in `backend/app/apps/common/models.py` publishing booking/fine events. |
| Abstract Factory | `PaymentProviderFactory` returning mock payment providers (`backend/app/apps/payments/services.py`). |
| Builder | `InvoiceBuilder` assembling invoice totals in `backend/app/apps/bookings/services.py`. |

The service layer (e.g., `BookingService`) encapsulates domain logic, keeping serializers/views slim and aligning with GRASP/SOLID principles.

## Frontend overview

The React single-page app offers:
- Car catalogue with quote widget.
- Customer dashboard for active bookings and invoices.
- Manager view to confirm, check-in, and complete rentals.
- Reporting page for utilization and financial summaries.

Authentication state is stored in a small Zustand store and automatically applied to API requests.

## Testing

Backend tests focus on the pricing pipeline and booking service state transitions:
```bash
cd backend
pytest
```

## Notes

- PostgreSQL runs in Docker; for local development without Docker, update `backend/.env` accordingly.
- The seed command populates sample users, cars, pricing rules, and a pending booking to explore the full flow.
- Additional enhancements like detailed validation, email notifications, and richer UI components can be layered on top of this foundation.
