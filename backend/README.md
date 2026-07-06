# Mirage Backend

FastAPI backend for the Mirage healthcare platform.

## Quick Start

1. Install dependencies:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Run migrations:
   ```bash
   alembic upgrade head
   ```

3. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://postgres:postgres@localhost:5432/mirage` |
| `TEST_DATABASE_URL` | PostgreSQL connection string for tests | `postgresql+asyncpg://postgres:postgres@localhost:5432/mirage_test` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |
| `JWT_SECRET` | Secret key for JWT signing | `change-me-jwt-secret` |
| `SECRET_KEY` | Alias for `JWT_SECRET` | |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token TTL | `60` |
| `REFRESH_SECRET` | Refresh token secret | `change-me-refresh-secret` |
| `DEMO_MODE` | Enable demo seeding | `false` |
| `AI_PROVIDER` | AI provider name | `mock` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `BCRYPT_ROUNDS` | Bcrypt hashing rounds | `12` |

## Running Tests

```bash
pytest tests/
```

## Database Commands

- Generate migration:
  ```bash
  alembic revision --autogenerate -m "Description"
  ```
- Upgrade to latest:
  ```bash
  alembic upgrade head
  ```
- Downgrade:
  ```bash
  alembic downgrade -1
  ```
