# InsightOps Review Hub — Portfolio Case Study

## Overview

InsightOps Review Hub is a compact full-stack knowledge operations application built to show production-minded engineering across backend architecture, typed frontend integration, operational workflow design, deterministic AI-system structure, testing, Docker delivery, and CI.

The product supports a complete internal review workflow:
- create workspace
- store source material
- generate excerpts
- create briefing request
- generate citation-backed answer
- persist evaluation
- record human review decision
- inspect audit history

## Why this project exists

Many repositories can demonstrate CRUD. Fewer repositories clearly demonstrate controlled AI output, traceability, reviewability, and operational governance in one end-to-end system.

This project was intentionally designed to prove:
- owner-scoped access control
- normalized relational design
- deterministic generation without external keys
- separation of automated evaluation from human review
- visible citations
- visible audit history
- typed React integration
- operationally credible UI
- reproducible local and Docker setup

## Architecture summary

### Backend
The backend is a Django and Django REST Framework application organized into explicit app boundaries:
- users
- workspaces
- sources
- briefings
- evaluations
- audit
- api

The API layer is split into serializers, permissions, selectors, services, views, and urls. This keeps business logic out of views and makes the repository easier to review and extend.

### Frontend
The frontend is a typed React and TypeScript application using:
- React Router
- TanStack Query
- Zustand
- Axios
- Zod-ready typed contracts

The interface is intentionally styled as an internal control surface rather than a tutorial dashboard.

## AI workflow design

The core demo path does not depend on any external API key.

Instead, the repository uses a deterministic stub flow:
1. source text is chunked into excerpts
2. briefing question terms are matched against excerpt terms
3. top excerpts are selected
4. a structured answer is composed
5. normalized citation rows are stored
6. heuristic evaluation scores are persisted
7. reviewer decisions are stored independently

This design keeps the repository runnable everywhere while still demonstrating the architecture of a grounded answer-generation system.

## Data modeling decisions

The strongest modeling decisions in the repository are:

- custom user model before first migration
- workspace ownership as the root access-control boundary
- normalized `AnswerCitation` rows rather than JSON citation references
- separate `EvaluationRun` and `ReviewDecision` tables
- append-only `AuditEvent` history

These decisions make the workflow reviewable and traceable.

## Testing strategy

The repository includes:
- Django tests
- pytest coverage
- Vitest component and route tests
- Playwright smoke flow

This provides confidence across model logic, API behavior, frontend rendering, and end-to-end workflow execution.

## Delivery and operations

The repository supports:
- SQLite for fast local development
- PostgreSQL through Docker Compose
- containerized backend and frontend
- GitHub Actions CI
- screenshot-ready seeded data

## Outcome

InsightOps Review Hub demonstrates a full-stack internal product that is compact, reviewable, operationally credible, and aligned with modern engineering expectations around traceability, testing, delivery discipline, and AI workflow governance.