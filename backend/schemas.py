"""
schemas.py
----------
Defines how data is sent and received via the API.
This prevents bad or malformed input.
"""

from pydantic import BaseModel
from datetime import date
from typing import Optional

class DailyLogCreate(BaseModel):
    log_date: date
    mood: Optional[int]
    sleep_hours: Optional[float]
    steps: Optional[int]
    notes: Optional[str]

class DailyLogResponse(DailyLogCreate):
    id: int

    class Config:
        orm_mode = True

