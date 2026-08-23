# Aether API Reference

The local FastAPI service exposes the following endpoints for data ingestion, review, and querying.

## Core Endpoints

### `POST /api/v1/events/batch`
Ingests a batch of raw activity events from background collectors.
- **Payload**: JSON array of activity events.
- **Action**: Stores the events as pending `RawEvent`s in the local SQLite database.

### `GET /api/v1/events/pending`
Fetches pending events for the Human Review Gate.
- **Action**: Returns a list of `RawEvent`s that have not yet been approved or purged.

### `POST /api/v1/review/approve`
Approves specific events for pipeline structuring and synthesis.
- **Payload**: Event IDs and any redactions.
- **Action**: Marks the selected events as approved. Approved events are subsequently processed by Agent A (`structuring.pipe`).

### `POST /api/v1/review/purge`
Hard-deletes sensitive events.
- **Payload**: Event IDs to purge.
- **Action**: Permanently deletes the raw events from the local database.

## Additional Endpoints

- `GET /health` - Health check.
- `PATCH /api/v1/events/{id}` - Modify/redact a pending event.
- `DELETE /api/v1/events/{id}` - Purge a specific pending event.
- `POST /api/v1/pipeline/structure` - Manually trigger Agent A structuring.
- `POST /api/v1/pipeline/synthesize` - Manually trigger Agent B synthesis.
- `GET /api/v1/summaries/{date}` - Retrieve the synthesized narrative for a specific date.
- `POST /api/v1/search` - Perform a semantic search query over approved memory.
- `GET /api/v1/settings` - Retrieve local configuration and retention settings.
- `PATCH /api/v1/settings` - Update configuration settings.
