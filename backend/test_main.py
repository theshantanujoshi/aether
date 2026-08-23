import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
import os

from main import app, get_db
from database import Base, RawEvent

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    # Create the test database and tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop all tables after tests
    Base.metadata.drop_all(bind=engine)
    TestingSessionLocal.close_all()
    engine.dispose()
    # Remove test.db file if it exists
    if os.path.exists("./test.db"):
        os.remove("./test.db")

def test_ingest_batch_success():
    """Happy path: ingest a batch of events."""
    response = client.post("/api/v1/events/batch", json={
        "source": "test_source",
        "events": [{"type": "user_signup", "user_id": 1}, {"type": "user_login", "user_id": 1}]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["count"] == 2
    
    # Check if events were actually saved to the db
    db = TestingSessionLocal()
    events = db.query(RawEvent).all()
    assert len(events) == 2
    assert events[0].source == "test_source"
    db.close()

def test_ingest_batch_empty_events():
    """Edge case: batch has no events."""
    response = client.post("/api/v1/events/batch", json={
        "source": "test_empty_source",
        "events": []
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["count"] == 0

def test_ingest_batch_invalid_input():
    """Error case: invalid schema."""
    response = client.post("/api/v1/events/batch", json={
        "source": "test_source",
        # missing 'events'
    })
    assert response.status_code == 422 # Pydantic validation error

def test_get_pending_events():
    """Happy path: get pending events."""
    # Insert a couple of events directly
    db = TestingSessionLocal()
    evt1 = RawEvent(source="s1", payload=json.dumps({"key": "val1"}), status="pending")
    evt2 = RawEvent(source="s2", payload=json.dumps({"key": "val2"}), status="approved")
    db.add(evt1)
    db.add(evt2)
    db.commit()
    db.close()

    response = client.get("/api/v1/events/pending")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["source"] == "s1"
    assert data[0]["payload"] == {"key": "val1"}

def test_approve_events():
    """Happy path: approve events."""
    db = TestingSessionLocal()
    evt1 = RawEvent(source="s1", payload="{}", status="pending")
    evt2 = RawEvent(source="s2", payload="{}", status="pending")
    db.add(evt1)
    db.add(evt2)
    db.commit()
    
    event_ids = [evt1.id, evt2.id]
    db.close()

    response = client.post("/api/v1/review/approve", json=event_ids)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["approved"] == 2

    # Verify they were approved
    db = TestingSessionLocal()
    events = db.query(RawEvent).all()
    assert all(e.status == "approved" for e in events)
    db.close()

def test_purge_events():
    """Happy path: purge events."""
    db = TestingSessionLocal()
    evt = RawEvent(source="s1", payload="{}", status="pending")
    db.add(evt)
    db.commit()
    event_id = evt.id
    db.close()

    response = client.post("/api/v1/review/purge", json=[event_id])
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["deleted"] == 1

    # Verify deleted
    db = TestingSessionLocal()
    events = db.query(RawEvent).all()
    assert len(events) == 0
    db.close()
