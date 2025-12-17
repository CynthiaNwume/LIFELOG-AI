"""
main.py
-------
Entry point for the FastAPI backend.
Defines API routes and business logic.
"""
from .ai_insights import generate_weekly_insight

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .database import SessionLocal
from .models import DailyLog
from .schemas import DailyLogCreate, DailyLogResponse

app = FastAPI(title="LifeLog AI Backend")

# Dependency to get a DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Health check endpoint
@app.get("/")
def read_root():
    return {"status": "LifeLog backend running"}

# Create a new daily log
@app.post("/log-day", response_model=DailyLogResponse)
def create_log(log: DailyLogCreate, db: Session = Depends(get_db)):
    # Check if log for that date already exists
    existing = db.query(DailyLog).filter(DailyLog.log_date == log.log_date).first()
    if existing:
        raise HTTPException(status_code=400, detail="Log for this date already exists")

    new_log = DailyLog(**log.dict())
    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    return new_log

# Get all logs
@app.get("/logs", response_model=List[DailyLogResponse])
def get_logs(db: Session = Depends(get_db)):
    return db.query(DailyLog).order_by(DailyLog.log_date.desc()).all()

@app.get("/insights/weekly")
def get_weekly_insights(db: Session = Depends(get_db)):
    # Get last 7 logs
    logs = (
        db.query(DailyLog)
        .order_by(DailyLog.log_date.desc())
        .limit(7)
        .all()
    )

    insight = generate_weekly_insight(logs)
    return {"insight": insight}
