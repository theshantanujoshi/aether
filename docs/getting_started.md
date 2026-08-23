# Getting Started with Aether

This guide covers the initial setup and configuration of Aether.

## Prerequisites

- Node.js (for React frontend)
- Python 3.9+ (for FastAPI backend)
- Qdrant or LanceDB (local vector database)
- [RocketRide Pipeline Builder](https://rocketride.io)

## Environment Configuration

The backend relies on environment variables set in `backend/.env` for runtime AI execution. You can copy the `backend/env.example` to `backend/.env` and configure the following variables:

- `ROCKETRIDE_URI`: Endpoint for the RocketRide engine
- `ROCKETRIDE_APIKEY`: Application authentication key
- `ROCKETRIDE_OPENAI_KEY`: LLM authentication (e.g., OpenRouter, OpenAI)
- `ROCKETRIDE_OPENAI_BASE_URL`: Target API Base (e.g., OpenRouter base URL)
- `ROCKETRIDE_OPENAI_MODEL`: Target model (e.g., Claude 3 Haiku)
- `ROCKETRIDE_QDRANT_HOST`: Local Vector DB host (e.g., localhost:6333)

## Running the Application

### Backend

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Activate your virtual environment and install dependencies (if not already done).
3. Start the FastAPI server (e.g., using `uvicorn`):
   ```bash
   uvicorn main:app --reload
   ```
The backend API binds exclusively to localhost for security and privacy.

### Frontend

1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies (e.g., `npm install`).
3. Start the Vite development server:
   ```bash
   npm run dev
   ```

## Next Steps

Once the application is running, the background collectors will begin submitting events to the ingestion API. Navigate to the React dashboard to review pending activity at the **Human Privacy Gate**.
