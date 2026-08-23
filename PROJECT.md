# Aether
**Project Specifications (A to Z)**

## 1. Executive Summary
**Vision**: A privacy-first personal activity intelligence system that turns fragmented local digital exhaust (terminal activity, browser history, notes, screenshots) into a searchable, narrative daily recap without requiring raw personal data to leave the user's machine.
**Core Principle**: Raw activity stays local by default; nothing becomes permanent memory without explicit human approval.

## 2. Architecture & Tech Stack
The architecture spans a local-first ingestion service, a Human Privacy Gate, and two primary AI agents configured via RocketRide pipelines.

### Frontend
- **Framework**: React + Vite
- **Language**: TypeScript
- **Linting**: Oxlint (`oxlint-tsgolint`)
- **Location**: `/frontend`

### Backend
- **Framework**: FastAPI (Python)
- **Database**: SQLite (via SQLAlchemy for storing `RawEvent` batches)
- **Testing**: pytest
- **Location**: `/backend`

### AI Pipelines & Vector Memory
- **Orchestration**: RocketRide Pipeline Builder (`.pipe` JSON definitions)
- **LLM Provider**: OpenRouter/OpenAI (configured dynamically via `.env`)
- **Vector Database**: Qdrant (via local instance on port 6333) / LanceDB
- **Pipelines**:
  - `structuring.pipe`: Ingests and structures approved raw events into normalized objects.
  - `synthesis.pipe`: Analyzes structured events to build a daily narrative/recap.

## 3. The Core Workflow (A to Z)
1. **Local Collection (A)**: Collectors (Terminal, Browser, Notes, Screenshots) gather activity.
2. **Ingestion (B)**: Events are POSTed to the backend via `/api/v1/events/batch` and stored as pending `RawEvent`s in SQLite.
3. **Human Review Gate (C)**: The React dashboard displays the pending batch. Users manually approve, redact, or purge data. Purged data is permanently hard-deleted.
4. **Structuring / Agent A (D)**: Approved data is routed through the `structuring.pipe` to detect context, deduplicate, and store as normalized entities (into the Qdrant vector database).
5. **Synthesis / Agent B (E)**: Periodically, `synthesis.pipe` processes the structured events to construct a cohesive daily narrative (Workstreams, Open Loops, Timeline).
6. **Semantic Search (Z)**: Users query their synthesized history natively in the dashboard through natural-language embeddings.

## 4. API Endpoints
The backend currently exposes the following endpoints:
- `POST /api/v1/events/batch` - Ingest activity
- `GET /api/v1/events/pending` - Fetch pending events for the review gate
- `POST /api/v1/review/approve` - Approve specific events for pipeline synthesis
- `POST /api/v1/review/purge` - Hard-delete sensitive events

## 5. Environment & Configurations
The backend relies on environment variables set in `backend/.env` for runtime AI execution:
- `ROCKETRIDE_URI` - Endpoint for the RocketRide engine
- `ROCKETRIDE_APIKEY` - Application auth
- `ROCKETRIDE_OPENAI_KEY` - LLM authentication (OpenRouter/OpenAI)
- `ROCKETRIDE_OPENAI_BASE_URL` - Target API Base (e.g., OpenRouter)
- `ROCKETRIDE_OPENAI_MODEL` - Target model (e.g., Claude 3 Haiku)
- `ROCKETRIDE_QDRANT_HOST` - Local Vector DB host

## 6. Security & Privacy
- **Local-First Posture**: API endpoints bind exclusively to localhost.
- **Untrusted Input**: Captured activity is treated strictly as data to prevent Prompt Injections during LLM synthesis.
- **Advisory PII Detection**: The frontend highlights likely secrets, but the user always acts as the final gate.
- **No Silent Uploads**: No raw unapproved event ever touches the embedding engine, Agent A/B, or optional remote backups.

## 7. Success Criteria & Milestones
- **Milestone 1**: Local Foundation (Ingestion, basic FastAPI, SQLite schema).
- **Milestone 2**: Privacy Gate (Staging batches, Review UI, Purge actions).
- **Milestone 3**: AI Pipeline (Agent A, Agent B, pipelines configured, Daily narrative).
- **Milestone 4**: Searchable Memory (Qdrant/LanceDB, semantic search, retrieval).
- **Milestone 5**: Hardening & Encryption (Client-side encryption, remote backups).
