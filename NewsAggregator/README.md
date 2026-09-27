# NewsAggregator

A simple News Aggregator app with a React frontend and a Python + FastAPI backend.

## Structure

- `frontend/`: React + Vite UI
- `backend/`: FastAPI API server

## Run locally

1. Start backend:
   - `cd NewsAggregator/backend`
   - `python -m venv .venv`
   - Activate the environment and install dependencies:
     - Windows: `.\.venv\Scripts\Activate.ps1`
     - `pip install -r requirements.txt`
   - `uvicorn backend.main:app --reload --port 8000`

2. Start frontend:
   - `cd NewsAggregator/frontend`
   - `npm install`
   - `npm run dev`

The frontend is configured to proxy `/api` requests to the FastAPI backend.
