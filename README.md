# FastAPI Call Ingestion Service (AI-PBX)

## Overview
A FastAPI-based microservice that ingests streaming call metadata, validates packet order, safely handles concurrent requests, and triggers background AI processing without blocking ingestion.

---

## Methodology
The service prioritizes fast, non-blocking ingestion and fault tolerance:

- Packets are accepted even if they arrive out of order
- Inconsistencies are logged, not rejected
- AI processing is handled asynchronously
- Database-level concurrency control ensures correctness under load

---

## Technical Details

- FastAPI with async endpoints
- PostgreSQL with Async SQLAlchemy
- Packet ingestion via `POST /v1/call/stream/{call_id}`
- Packet order tracked using `last_sequence`
- Row-level locking and unique-constraint recovery to handle race conditions
- Simulated flaky AI service with random latency and retry logic
- Integration test simulates concurrent packet arrivals for the same `call_id`

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- PostgreSQL running locally

### Run Locally
```bash```
git clone <repo-url>
cd app
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
createdb calls_db
uvicorn app.main:app --reload

---

API Docs: http://127.0.0.1:8000/docs

---

Run Tests: pytest app/tests

---

Notes
	•	Out-of-order packets are logged but still accepted
	•	Concurrent inserts are handled safely using database transactions
	•	Startup event deprecation warnings are expected and do not affect functionality
