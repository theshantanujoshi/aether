import json
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Any
import rocketride as rr

from database import init_db, get_db, RawEvent

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="RocketRide Data Synthesizer API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the RocketRide Data Synthesizer API. Visit /docs for the API documentation."}

class EventBatch(BaseModel):
    source: str
    events: List[dict]

@app.post("/api/v1/events/batch")
def ingest_batch(batch: EventBatch, db: Session = Depends(get_db)):
    count = 0
    for evt in batch.events:
        db_evt = RawEvent(source=batch.source, payload=json.dumps(evt))
        db.add(db_evt)
        count += 1
    db.commit()
    return {"status": "success", "count": count}

@app.get("/api/v1/events/pending")
def get_pending(db: Session = Depends(get_db)):
    events = db.query(RawEvent).filter(RawEvent.status == "pending").all()
    return [{"id": e.id, "source": e.source, "timestamp": e.timestamp, "payload": json.loads(e.payload)} for e in events]

@app.post("/api/v1/review/approve")
def approve_events(event_ids: List[int], db: Session = Depends(get_db)):
    # In a real app we would send these to RocketRide Agent A here via rr.Client().send()
    # For MVP we just mark them approved
    events = db.query(RawEvent).filter(RawEvent.id.in_(event_ids)).all()
    
    # client = rr.Client()
    # client.send("b992f036-71d3-4f51-b0be-d30f40d85ab2", data=json.dumps([e.payload for e in events]))
    
    for e in events:
        e.status = "approved"
    db.commit()
    return {"status": "success", "approved": len(events)}

@app.post("/api/v1/review/purge")
def purge_events(event_ids: List[int], db: Session = Depends(get_db)):
    events = db.query(RawEvent).filter(RawEvent.id.in_(event_ids)).all()
    for e in events:
        db.delete(e) # Hard delete
    db.commit()
    return {"status": "success", "deleted": len(events)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
