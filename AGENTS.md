# 🤖 AGENTS.md

This document defines the standards, structure, and expectations for human contributors and AI agents working on the `silph-users` microservice.  
Everything here is intentional. Please follow carefully to ensure clean, secure, and maintainable code.

---

## 🧠 Coding Philosophy

This service follows the core principles of:

- **KISS** – Keep it simple and self-explanatory
- **DRY** – Don’t repeat yourself
- **Clarity over cleverness** – Prioritize readability
- **Explicit over implicit** – Avoid magic
- **Secure by default** – No shortcuts for user auth
- **Well-documented** – Docstrings for all logic-bearing functions

---

## 🔧 Guidelines

- Use **Python 3.11+** with consistent **PEP8-style formatting**
- Always include **type hints** and **docstrings** for all public functions, classes, and modules
- Prefer **async** logic where applicable (e.g. database, route handlers)
- Keep functions small, testable, and focused on one purpose
- Use Pydantic models for all input/output schemas
- Centralize shared logic in services (not utils unless they're truly generic)
- Avoid global state, circular imports, and deeply nested logic

---

## 📁 Expected Folder Structure (starting baseline)

app/
├── main.py # FastAPI entrypoint
├── api/ # Route handlers (e.g., auth, users)
├── models/ # SQLAlchemy models
├── schemas/ # Pydantic request/response schemas
├── services/ # Business logic (e.g., AuthService)
├── db/ # DB session and connection logic
├── core/ # Config, auth utils, constants
├── tests/ # Test suite
└── version.json # Service metadata

This structure will evolve with features (e.g. roles, password reset) but should remain consistent and modular.

---

## 🔒 Security Expectations

- Hash passwords using **bcrypt** or **Argon2** via `passlib`
- Use **`python-jose`** or similar for JWT encoding/decoding
- Validate all input via Pydantic schemas
- Never trust raw request data — always sanitize and validate
- Protect all routes with proper auth decorators/dependencies
- No hardcoded secrets, credentials, or ports — use `.env`
- Implement secure CORS settings and use HTTPS in production

---

## ⚙️ Development Rules

- Containerized via Docker and Docker Compose (dev must match prod structure)
- App config should be fully environment-driven (`config.py` + `.env`)
- Separate `access` and `refresh` token logic
- Structure auth logic into a clean service layer, not in routes
- All services should expose `/health` and `/version` endpoints
- Use `pytest` + `httpx` for testing (especially for endpoint testing)
- Mark all unfinished logic with `# TODO` or `raise NotImplementedError()`

---

## 🤖 AI Agent-Specific Notes

If you're an AI agent writing or modifying code:

- Do **not** assume structure — check this file or ask
- Always add docstrings for any code you generate
- Prefer clarity over abstraction unless abstraction is justified by repeated use
- Avoid generating placeholder business logic unless clearly marked
- Structure new logic within existing service boundaries — don’t invent modules

---

## 📌 Updates

This document will evolve as the `silph-users` service matures. Updates here are binding for this service only.  
For cross-service standards, refer to the `silph-docs` system-wide spec (if/when created).