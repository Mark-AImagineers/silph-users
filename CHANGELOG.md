# 📓 Changelog

All notable changes to `silph-users` will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2025-07-01

### Added
- Initial project scaffold
- Base folder structure
- README and changelog templates

---
## [0.1.1] - 2025-07-01

### Added
- Environment-driven config using `pydantic-settings`
- Database connection via `asyncpg` and SQLAlchemy
- Password hashing and verification using `bcrypt`
- User model and migration-ready table schema
- User registration with email/username uniqueness checks
- User login with JWT access and refresh token generation
- `/auth/me` endpoint using reusable `get_current_user()` logic
- `/health` and `/version` system endpoints
- Full container setup via Docker and Docker Compose
- Initial security layers: token-based auth, input validation, hashed passwords

---
## [0.1.2] - 2025-07-01

### Added
- Expired or blacklisted token handling

---
## 🧭 Planned Items

This section lists all major components to be implemented over time to complete the `silph-users` service.

- Alembic migrations (optional)
- Public user profile retrieval (optional)
- User profile update endpoint
- Role/claim system for authorization context
- Request logging and structured error responses
- Rate limiting (optional, e.g. login abuse prevention)
- Unit and integration test coverage
- OpenAPI schema polishing
- CI test runner integration (e.g. GitHub Actions)
- Future-ready: social login stub endpoints
- Future-ready: password reset token flow
- Future-ready: user deletion or anonymization
- Future-ready: admin-level access override
- Added Security - Consider - Argon2, LockBox, Rate Limiting, Rehash Detection, Pepper, obscure DB

















---

TEMPLATE:
## [0.1.1] - YYYY-MM-DD

### Fixed
- Example: Corrected missing environment variable validation

---

## [0.2.0] - YYYY-MM-DD

### Added
- Example: User profile update endpoint
- Example: Role claim support for token payload

---

_Replace `YYYY-MM-DD` with release dates when versions are published._

