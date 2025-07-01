# silph-users

User service for **Project Silph** — manages registration, authentication, and user profiles. Implements JWT-based access control and is designed for secure, standalone deployment as part of a microservice architecture. Designed as a standalone FastAPI application, silph-users is intended to be deployed independently within a microservices architecture. It communicates with other services via secure APIs and is built with future extensibility in mind — including support for:

- Role- and permission-based access control
- Social login integrations
- Audit logging and account recovery features
- Full localization for Filipino users

Security and modularity are top priorities — this service is structured to be testable, maintainable, and production-ready from the start.

---

## 🧩 Role and Purpose

`silph-users` is the **identity and authentication service** within the Project Silph microservices architecture. Its sole responsibility is to manage:

- **User identity** — creation, storage, and retrieval of user records
- **Authentication** — credential verification and JWT issuance
- **Authorization context** — validating and refreshing tokens, exposing user claims
- **Basic profile data** — usernames, emails, and optional public info

In short:  
`silph-users` owns who the user is, how they're authenticated, and what other services need to know about them.

---
## 🛠 Tech Stack

This service is **backend-only** and built for performance, modularity, and clear API boundaries.

- **Language:** Python 3.11+
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy (async)
- **Auth:** `python-jose` for JWT encoding/decoding
- **Documentation:** Auto-generated via OpenAPI (`/docs`)
- **Containerization:** Docker / Docker Compose
- **Testing:** `pytest` + `httpx` for unit and integration tests