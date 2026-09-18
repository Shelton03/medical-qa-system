# Mirage
# Project Index

Version: 1.0

---

# Purpose

Welcome to the Mirage project.

This document is the entry point for the entire repository and should be the **first document read** by any engineer or AI coding assistant before implementation begins.

It defines:

- The project vision
- Documentation hierarchy
- Reading order
- Source-of-truth precedence
- Implementation phases
- Success criteria

Every other document assumes this file has already been read.

---

# Project Overview

Mirage is a healthcare platform designed to improve patient-doctor interactions through secure, real-time collaboration and AI-assisted clinical workflows.

The system consists of two primary applications:

## Patient Application

A mobile-first web application rendered inside a realistic simulated phone frame.

The patient application allows users to:

- Log in securely
- Complete an AI-powered symptom assessment
- Receive consent requests
- Approve or deny access to medical records
- Participate in consultations
- View medical history
- Review consultation summaries
- Receive notifications

The application is intentionally designed to mimic a native mobile application while running entirely in the browser.

---

## Doctor Portal

A desktop-first clinical dashboard.

Doctors can:

- Search for patients
- Request consent
- Review patient timelines
- Conduct consultations
- Generate AI-assisted documentation
- Finalize consultation notes
- Update medical records
- Monitor notifications

---

## Demonstration Mode

The repository also includes a split-screen demonstration mode.

This mode displays:

Patient Application

↓

Doctor Portal

side by side.

The purpose is to demonstrate:

- Consent workflow
- Real-time synchronization
- AI assistance
- Notification delivery
- Medical record updates

without requiring multiple physical devices.

---

# Technology Stack

## Backend

- Python 3.12+
- FastAPI
- SQLAlchemy 2.x
- PostgreSQL
- Redis
- Alembic
- JWT Authentication

---

## Frontend

- Next.js
- TypeScript
- TailwindCSS
- Framer Motion
- React Query
- React Hook Form
- Zod

---

## Infrastructure

- Docker
- Docker Compose

The repository should run locally using a single command:

```
docker compose up
```

---

# AI Architecture

The system integrates multiple AI capabilities.

These include:

- Existing Symptom Checker
- Transcription
- Clinical Summaries
- Diagnostic Suggestions

These services are **not implemented directly**.

Instead they are abstracted behind provider interfaces.

Business logic must never depend directly on any AI vendor SDK.

---

# Documentation Structure

The repository documentation consists of the following files.

```
docs/

00_Project_Index.md

01_Product_Requirements_Document.md

02_Technical_Architecture.md

03_Design_System.md

04_Implementation_Plan.md

05_API_Contract.md

06_Database_Schema.md

07_Master_Generation_Prompt.md

08_Coding_Standards.md

09_Deployment_Guide.md

10_UI_Screen_Specification.md

11_User_Flows_and_State_Machines.md

12_Appointment_Booking_System.md
```

Each document has a distinct responsibility.

---

# Reading Order

Documentation should be read in the following order.

Project Index

↓

Product Requirements

↓

Technical Architecture

↓

Design System

↓

Implementation Plan

↓

API Contract

↓

Database Schema

↓

Master Generation Prompt

↓

Coding Standards

↓

Deployment Guide

↓

UI Screen Specification

↓

User Flows and State Machines

↓

Appointment Booking System

This order is intentional.

Later documents assume knowledge established by earlier documents.

---

# Document Responsibilities

## 00 — Project Index

Defines the project and documentation hierarchy.

---

## 01 — Product Requirements

Defines the product vision, user journeys, functional requirements, and success criteria.

---

## 02 — Technical Architecture

Defines system architecture, services, providers, repositories, and infrastructure.

---

## 03 — Design System

Defines the visual language, mobile simulation, components, animations, spacing, and interaction patterns.

---

## 04 — Implementation Plan

Defines implementation phases and build order.

---

## 05 — API Contract

Defines every REST endpoint, request, response, WebSocket event, and authentication rule.

---

## 06 — Database Schema

Defines the relational database model and persistence layer.

---

## 07 — Master Generation Prompt

Defines how an AI coding assistant should think, reason, and generate the repository.

---

## 08 — Coding Standards

Defines engineering conventions for backend, frontend, testing, and collaboration.

---

## 09 — Deployment Guide

Defines local development, Docker, production deployment, monitoring, backups, and scaling.

---

## 10 — UI Screen Specification

Defines every screen, widget, navigation flow,
loading state, empty state and API dependency.

---

## 11 — User Flows and State Machines

Defines the lifecycle and transitions for
authentication, consent, consultation,
notifications and AI workflows.

---

## 12 — Appointment Booking System

Defines the appointment booking feature including
patient booking flow, auto-routing algorithm,
doctor scheduling, admin management, and
database schema changes.

---

# Source of Truth Priority

If documentation appears to conflict, use the following order of precedence.

1.

Product Requirements

↓

2.

Technical Architecture

↓

3.

API Contract

↓

4.

Database Schema

↓

5.

Design System

↓

6.

Implementation Plan

↓

7.

Coding Standards

↓

8.

Deployment Guide

The Master Generation Prompt should always operate within the constraints of these documents.

It must never override the documented requirements.

---

# Development Principles

The repository should prioritize:

- Maintainability
- Readability
- Extensibility
- Security
- Accessibility
- Performance
- Testability

Avoid unnecessary complexity.

Build for long-term maintainability rather than rapid prototyping.

---

# AI Coding Assistant Workflow

When generating the repository, follow this process:

1. Read every documentation file.
2. Build the repository incrementally according to the Implementation Plan.
3. Ensure each phase compiles before moving to the next.
4. Preserve architectural consistency.
5. Generate tests alongside implementation.
6. Update documentation when implementation changes.
7. Refactor where appropriate before proceeding.

Do not skip phases or generate unrelated features.

---

# Repository Deliverables

The completed repository should include:

- Backend application
- Frontend application
- Docker Compose configuration
- PostgreSQL integration
- Redis integration
- JWT authentication
- Demo mode authentication
- Provider abstractions
- Existing symptom checker integration
- AI provider interfaces
- WebSocket communication
- Split-screen demonstration
- PhoneFrame mobile simulator
- Doctor dashboard
- Patient application
- Unit tests
- Integration tests
- Documentation
- Database migrations
- Seed data

---

# Success Criteria

The project is considered complete when:

- All Product Requirements have been implemented.
- Docker Compose starts the complete system.
- Database migrations execute successfully.
- Seed data loads correctly.
- Demo mode works.
- JWT authentication works.
- Patient and doctor workflows are complete.
- Consent workflow synchronizes in real time.
- AI integrations remain provider-agnostic.
- All tests pass.
- Documentation is complete.
- The repository can be cloned and run without undocumented setup.

---

# Final Objective

Mirage should resemble a production-quality healthcare platform built by an experienced engineering team.

The generated repository should be coherent, maintainable, well-documented, and ready for future expansion beyond the demonstration environment.

# End of Project Index