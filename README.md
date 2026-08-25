# Aether 

A privacy-first personal activity intelligence system that turns fragmented local digital exhaust—terminal activity, browser history, notes, screenshots, and app logs—into a searchable, narrative daily recap without requiring raw personal data to leave the user's machine.

## Core Principle

> **Raw activity stays local by default; nothing becomes permanent memory without explicit human approval.**

## Documentation

Comprehensive documentation can be found in the `/docs` directory:

- [Getting Started](docs/getting_started.md)
- [Architecture](docs/architecture.md)
- [API Reference](docs/api.md)
- [Security & Privacy](docs/security_and_privacy.md)

## What is Aether?

Independent researchers, developers, and power users generate substantial amounts of digital activity across disconnected tools. Today, this activity is fragmented across applications and difficult to reconstruct later. 

Aether addresses this with a local-first ingestion and synthesis pipeline, combined with an explicit human review gate, creating a private "memory layer" over your digital work.

### Key Features

1. **Local-First Collection**: Background collectors periodically gather supported activity (Terminal, Browser, Markdown, Screenshots).
2. **Human Privacy Gate**: Review, approve, redact, or purge data before it enters permanent memory.
3. **AI Structuring & Synthesis**: Uses RocketRide pipelines to detect context, deduplicate, and store as normalized entities. Constructs a cohesive daily narrative.
4. **Semantic Search**: Natural-language queries over your synthesized history through vector embeddings (Qdrant/LanceDB).

## Quick Start Overview

Aether is composed of a FastAPI backend and a React frontend. The AI pipelines are orchestrated via RocketRide Pipeline Builder.

1. Configure environment variables in `backend/.env`.
2. Run the FastAPI server.
3. Access the React dashboard to review and search your activity.

See [Getting Started](docs/getting_started.md) for detailed setup instructions.
