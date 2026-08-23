# Aether Architecture

The Aether architecture spans a local-first ingestion service, a Human Privacy Gate, and two primary AI agents configured via RocketRide pipelines.

## High-Level Architecture Diagram

```text
┌───────────────────────────────────────────────────────────────┐
│                         LOCAL MACHINE                         │
│                                                               │
│  Terminal   Browser   Markdown   Screenshots   App Activity   │
│      │          │         │            │             │        │
│      └──────────┴─────────┴────────────┴─────────────┘        │
│                           │                                   │
│                    Local Ingestion                            │
│                           │                                   │
│                    FastAPI Endpoint                           │
│                           │                                   │
│                    Staging / Batch                            │
│                           │                                   │
│                    ┌──────▼──────┐                            │
│                    │ Human Gate  │                            │
│                    │ Review/Purge│                            │
│                    └──────┬──────┘                            │
│                           │ Approved only                     │
│                           ▼                                   │
│                 ┌────────────────────┐                        │
│                 │ Agent A: Structurer│                        │
│                 └─────────┬──────────┘                        │
│                           │                                   │
│                    Structured Events                          │
│                           │                                   │
│                 ┌─────────▼────────────┐                      │
│                 │ Agent B: Synthesizer │                      │
│                 └─────────┬────────────┘                      │
│                           │                                   │
│             ┌─────────────┴─────────────┐                     │
│             ▼                           ▼                     │
│       Daily Narrative              Embeddings                 │
│             │                           │                     │
│             ▼                           ▼                     │
│       React Dashboard              LanceDB/Qdrant             │
│             │                                                 │
│             └──────────────┬──────────────────────────────────┘
│                            │
│                 Optional encrypted backup
│                            │
└────────────────────────────▼───────────────────────────────────┘
                         Remote Server
```

## 1. Local Collection (Source Collectors)

Background collectors periodically gather supported activity. Raw data should remain on the user's machine.
- **Terminal**: Captures commands, timestamps, working directory, and outputs (excluding sensitive paths/patterns).
- **Browser**: Captures metadata such as URL and page title.
- **Markdown / Local Notes**: Captures file paths, modification times, and relevant content changes.
- **Screenshots**: Captures visual workspace contexts.

## 2. Ingestion

Events are batched and `POST`ed to the local FastAPI backend. They are stored as pending `RawEvent`s in SQLite, ready for review.

## 3. Human Review Gate

The React dashboard displays the pending batch. The user can manually approve, redact, or purge data. Purged data is permanently hard-deleted and never enters the downstream synthesis or memory layers.

## 4. Agent A: Structurer

Approved data is routed through the `structuring.pipe` RocketRide pipeline. 
- Normalizes inputs into chronological events.
- Deduplicates and detects project context.
- Stores normalized entities in the vector database (Qdrant or LanceDB).

## 5. Agent B: Synthesizer

Periodically, the `synthesis.pipe` processes the structured events to construct a cohesive daily narrative:
- Clusters events into workstreams.
- Identifies major accomplishments and open loops.
- Generates a human-readable recap of the day.

## 6. Semantic Search

Approved structured events and summaries are embedded locally. Users can query their synthesized history natively in the dashboard through natural-language semantic retrieval.
