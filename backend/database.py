from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./local_memory.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class RawEvent(Base):
    __tablename__ = "raw_events"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    payload = Column(Text) # JSON string
    status = Column(String, default="pending") # pending, approved, deleted

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
