"""
models.py
---------
Defines Python representations of database tables.
Each class = one table.
"""

from sqlalchemy import Column, Integer, Date, Text, TIMESTAMP
from sqlalchemy.sql import func
from .database import Base

class DailyLog(Base):
    __tablename__ = "daily_logs"

    id = Column(Integer, primary_key=True, index=True)
    log_date = Column(Date, unique=True, nullable=False)
    mood = Column(Integer)
    sleep_hours = Column(Integer)
    steps = Column(Integer)
    notes = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
