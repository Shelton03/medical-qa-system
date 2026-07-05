# Mirage
# Deployment Guide

Version: 1.0

---

# Purpose

This document defines how Mirage should be:

- Developed
- Configured
- Deployed
- Monitored
- Maintained

It serves as the operational handbook for both local development and future production deployments.

---

# Deployment Philosophy

Mirage should be deployable with minimal manual configuration.

A new developer should be able to clone the repository, configure environment variables, and launch the full stack using a single command.

Infrastructure should be reproducible and containerized.

---

# Technology Stack

Backend

- FastAPI
- Uvicorn

Frontend

- Next.js

Database

- PostgreSQL 16+

Cache

- Redis

Reverse Proxy

- Traefik (recommended) or Nginx

Container Runtime

- Docker

Orchestration

- Docker Compose (development)

Future Production

- Kubernetes-compatible architecture

---

# Local Development

Requirements

- Docker Desktop or Docker Engine
- Docker Compose v2+
- Git

No local installation of PostgreSQL or Redis should be required.

---

# Repository Layout

```
mirage/

backend/

frontend/

docs/

docker/

scripts/

docker-compose.yml

README.md

.env.example
```

---

# Development Startup

Clone the repository.

```
git clone <repository>
```

Create environment file.

```
cp .env.example .env
```

Start the system.

```
docker compose up --build
```

Expected services

- frontend
- backend
- postgres
- redis

Optional

- mailhog
- pgadmin
- minio

---

# Docker Services

## frontend

Purpose

Next.js application

Port

```
3000
```

---

## backend

Purpose

FastAPI API

Port

```
8000
```

Health endpoint

```
/health
```

---

## postgres

Purpose

Persistent database

Port

```
5432
```

Persistent Docker volume

```
postgres_data
```

---

## redis

Purpose

Caching

Pub/Sub

Background jobs

Port

```
6379
```

---

## mailhog (Development)

Purpose

Capture outbound email.

No real email should be sent during development.

Port

```
8025
```

---

## pgAdmin (Optional)

Purpose

Database inspection.

Should be disabled by default.

---

## MinIO (Optional)

Purpose

Local S3-compatible storage for uploaded files.

Used to validate provider abstraction before integrating cloud storage.

---

# Environment Variables

Backend

```
APP_ENV=development

DEBUG=true

SECRET_KEY=

JWT_SECRET=

JWT_ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60

REFRESH_TOKEN_EXPIRE_DAYS=30

DATABASE_URL=

REDIS_URL=

DEMO_MODE=true

SYMPTOM_PROVIDER=mock

AI_PROVIDER=mock

TRANSCRIPTION_PROVIDER=mock

EMAIL_PROVIDER=mailhog

STORAGE_PROVIDER=local
```

Frontend

```
NEXT_PUBLIC_API_URL=

NEXT_PUBLIC_WS_URL=

NEXT_PUBLIC_DEMO_MODE=true
```

Secrets must never be committed to source control.

---

# Database Migrations

Alembic should execute automatically during container startup when appropriate.

Manual commands

```
alembic revision --autogenerate

alembic upgrade head

alembic downgrade -1
```

Production deployments should always run pending migrations before serving traffic.

---

# Seed Data

Development environments should automatically load demo data.

Seed includes

- Patients
- Doctors
- Facilities
- Visits
- Medical records
- Notifications
- Consent requests
- AI sessions

Production must never load demo data automatically.

---

# Health Checks

Backend

```
GET /health
```

Should verify:

- Database connectivity
- Redis connectivity
- Provider initialization

Frontend

Simple readiness endpoint.

Docker Compose should wait for healthy dependencies before starting dependent services.

---

# Logging

All containers should emit structured logs to stdout/stderr.

Fields should include:

- Timestamp
- Request ID
- User ID (when available)
- Log level
- Service name
- Message

Avoid writing logs directly to files inside containers.

---

# Development Workflow

Typical workflow:

1. Start Docker Compose.
2. Apply database migrations.
3. Load seed data.
4. Run backend and frontend.
5. Execute automated tests.
6. Iterate on features.

The environment should support hot reloading for both backend and frontend where practical.

# Production Deployment

---

# Deployment Targets

The application should remain deployment-platform agnostic.

Recommended supported targets:

- Docker Compose (single-server deployments)
- DigitalOcean Droplets
- Azure Virtual Machines
- AWS EC2
- Google Compute Engine
- Kubernetes clusters (future)
- Azure Container Apps (future)

The application should not rely on vendor-specific infrastructure.

---

# Reverse Proxy

Production traffic should terminate at a reverse proxy.

Recommended:

- Traefik
- Nginx

Responsibilities:

- HTTPS termination
- Automatic certificate renewal
- Compression
- Security headers
- WebSocket proxying
- Rate limiting
- Static asset caching

---

# HTTPS

HTTPS is mandatory in production.

Certificates should be managed automatically using Let's Encrypt.

Enable:

- HTTP → HTTPS redirects
- HSTS
- TLS 1.2+
- Secure cookies
- SameSite cookie policy

---

# Authentication

Production configuration should disable Demo Mode.

```
DEMO_MODE=false
```

JWT signing keys should:

- Be randomly generated
- Be rotated periodically
- Never be committed to source control

Refresh tokens should:

- Be hashed before storage
- Be revocable
- Expire automatically

---

# File Storage

Storage is abstracted behind the StorageProvider interface.

Development

```
Local filesystem
```

Production

Supported providers:

- Amazon S3
- Azure Blob Storage
- Google Cloud Storage
- MinIO

Application code should remain unchanged when switching providers.

---

# Email Delivery

Development

MailHog

Production

Examples:

- SendGrid
- Amazon SES
- Azure Communication Services
- SMTP

The EmailProvider interface should isolate implementation details.

---

# AI Providers

The application should support multiple providers without changing business logic.

Possible implementations:

- Existing Symptom Checker
- OpenAI
- Azure OpenAI
- Anthropic
- Local LLMs
- Mock provider

Providers should be selected through configuration.

Example

```
AI_PROVIDER=openai
```

---

# Monitoring

Recommended stack

Metrics

- Prometheus

Visualization

- Grafana

Error Tracking

- Sentry

Structured Logs

- Loki (optional)

Health Monitoring

- Uptime Kuma (optional)

The application should expose metrics endpoints for future monitoring integrations.

---

# Backup Strategy

PostgreSQL

Nightly backup

Retention

30 days

Weekly backup

Retention

12 weeks

Monthly backup

Retention

12 months

Uploaded documents should follow the same retention policy where applicable.

Backups should be encrypted at rest.

---

# Disaster Recovery

Recovery procedure should include:

1.

Restore PostgreSQL database.

2.

Restore uploaded files.

3.

Restore environment variables.

4.

Run migrations if required.

5.

Verify application health.

Recovery documentation should be tested periodically.

---

# Scaling Strategy

The architecture should support horizontal scaling.

Stateless services:

- Backend API
- Frontend

Shared infrastructure:

- PostgreSQL
- Redis
- Object storage

Avoid storing session state in application memory.

Use Redis for distributed coordination where necessary.

---

# WebSocket Scaling

For multiple backend instances, WebSocket events should be distributed through Redis Pub/Sub.

This allows real-time updates regardless of which backend instance a client is connected to.

---

# Background Processing

Long-running operations should execute outside the request-response cycle.

Examples:

- AI summarization
- Audio transcription
- Email delivery
- Notification fan-out
- File processing

Recommended queue:

- Celery with Redis
- RQ with Redis

Workers should be independently scalable.

---

# Security Hardening

Production deployments should include:

- HTTPS only
- Security headers
- CORS restrictions
- Rate limiting
- Input validation
- Dependency vulnerability scanning
- Automatic security updates
- Principle of least privilege for service accounts

Database access should never be exposed publicly.

Redis should not be accessible from the public internet.

---

# Secrets Management

Secrets should never be stored in the repository.

Development

```
.env
```

Production

Examples:

- Docker Secrets
- Azure Key Vault
- AWS Secrets Manager
- HashiCorp Vault

Configuration should support secret rotation without code changes.

---

# Release Process

Recommended workflow:

1. Create feature branch.
2. Implement feature.
3. Run automated tests.
4. Review code.
5. Merge into main.
6. Build Docker images.
7. Apply database migrations.
8. Deploy updated containers.
9. Verify health checks.
10. Monitor logs and metrics.

Each release should be tagged using semantic versioning.

Example

```
v1.0.0
v1.1.0
v1.1.1
```

---

# CI/CD (Future)

Although not required for the initial demo, the repository should be structured to support future CI/CD pipelines.

Potential pipeline stages:

- Lint
- Type checking
- Unit tests
- Integration tests
- Build frontend
- Build backend
- Build Docker images
- Security scanning
- Push images
- Deploy
- Smoke tests

Pipeline configuration should be easy to add without restructuring the repository.

---

# Production Checklist

Before deploying to production, verify:

✓ Environment variables configured

✓ Database migrations applied

✓ Demo Mode disabled

✓ JWT secrets configured

✓ HTTPS enabled

✓ Reverse proxy configured

✓ Redis running

✓ AI providers configured

✓ Email provider configured

✓ Storage provider configured

✓ Logging enabled

✓ Monitoring enabled

✓ Backups configured

✓ Health checks passing

✓ Seed data disabled

✓ Test suite passing

✓ Security review completed

---

# Operational Checklist

Routine operational tasks include:

Daily

- Review application logs
- Monitor failed requests
- Verify backup completion

Weekly

- Review dependency updates
- Inspect audit logs
- Validate monitoring alerts

Monthly

- Test disaster recovery procedures
- Rotate secrets where appropriate
- Review infrastructure costs
- Archive old logs according to retention policy

---

# Definition of Successful Deployment

A deployment is considered successful when:

- All containers are healthy.
- Backend health checks pass.
- Frontend is accessible.
- Database connectivity is verified.
- Redis connectivity is verified.
- Authentication functions correctly.
- Demo Mode behaves according to configuration.
- Patient and doctor workflows complete successfully.
- Real-time consent updates synchronize correctly.
- AI providers respond through their abstraction layer.
- Notifications are delivered.
- Logs are being collected.
- Monitoring reports healthy services.
- No manual intervention is required after deployment.

---

# Final Objective

Mirage should be deployable, maintainable, and extensible from a single developer laptop to a production environment without requiring architectural changes.

Every deployment should be reproducible, documented, and observable.

The operational experience should be as polished as the application itself.

# End of Deployment Guide