“BookIt API”
Problem
Build a production-ready REST API for a simple bookings platform called BookIt. Users can browse services, make bookings, and leave reviews. Admins manage users, services, and bookings.

Core Entities
User: id, name, email, password_hash, role (user | admin), created_at
Service: id, title, description, price, duration_minutes, is_active, created_at
Booking: id, user_id, service_id, start_time, end_time, status (pending | confirmed | cancelled | completed), created_at
Review: id, booking_id, rating (1–5), comment, created_at
You PostgreSQL or MongoDB. Choose one and justify your choice in README.

Requirements
1) Authentication & Authorization
Register, login, logout/refresh using JWT.
Passwords hashed with a strong algorithm (e.g., bcrypt).
Role-based access:
user: can CRUD their own bookings and reviews.
admin: can CRUD services, view all bookings, change booking status.
Use appropriate headers (Authorization: Bearer <token>).
Return 401 for unauthenticated, 403 for unauthorized.
2) Database
Data validation at both the schema layer (Pydantic) and DB constraints where applicable.
For PostgreSQL: manage migrations with Alembic.
3) HTTP Methods & Status Codes (use correct ones!)
Implement at least the following endpoints with correct verbs and status codes:

Auth

POST /auth/register
POST /auth/login
POST /auth/refresh
POST /auth/logout
Users

GET /me (current user profile)
PATCH /me
Services (public read, admin manage)

GET /services (query: q, price_min, price_max, active)
GET /services/{id}
POST /services (admin)
PATCH /services/{id} (admin)
DELETE /services/{id} (admin)
Bookings

POST /bookings (user creates); validate overlaps/conflicts
GET /bookings (user: only theirs; admin: all, with filters status, from, to)
GET /bookings/{id} (owner or admin)
PATCH /bookings/{id} (owner can reschedule/cancel if pending or confirmed; admin can update status)
DELETE /bookings/{id} (owner before start_time; admin anytime)
Reviews

POST /reviews (must be for a completed booking by the same user, one review per booking)
GET /services/{id}/reviews
PATCH /reviews/{id} (owner)
DELETE /reviews/{id} (owner or admin)
4) Modular Design
Project layout (example):

Separate routers, services (business rules), and repositories (DB access). No DB code inside route handlers.
5) Production Deployment
Use environment variables for secrets and config (no secrets in code).
Add structured logging and basic request logging.
Deploy to a real host (pipeops)
Provide the public base URL and a live OpenAPI docs link in the README.
6) Testing (optional, for extra credit)
pytest with at least:
Auth flow tests (register/login/refresh/401/403 paths).
Booking conflict logic.
Permissions (user vs admin).
Happy & unhappy paths with status code assertions.
7) Documentation
Auto-generated docs (FastAPI Swagger/Redoc).
Hand-written README explaining:
Arch decisions, chosen DB.
How to run locally.
Env vars table.
Deployment notes (host, base URL).
Acceptance Criteria (what we’ll check)
Can register, login, and call protected endpoints with JWT.
Admin routes are protected; users cannot access them.
Booking conflict prevention works and returns 409 Conflict when appropriate.
All endpoints use correct HTTP methods and status codes consistently.
Codebase shows clean modular separation (routers/services etc).
Tests run with pytest and pass (optional but plus points).
Deliverables
Git repo link (public).
Production URL + docs URL.
README with setup, env, and decisions.



for the alembic migrationn,

alembic upgrade head

alembic revision --autogenerate -m "Sync database schema"