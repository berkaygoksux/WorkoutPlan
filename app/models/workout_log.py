from pydantic import BaseModel
from datetime import date
from typing import Optional

class WorkoutLogCreate(BaseModel):
    exercise_id: int
    exercise_name: str
    exercise_description: Optional[str] = None
    sets: int
    reps: int
    date: date
    duration: int
    notes: Optional[str] = None

class WorkoutLog(BaseModel):
    log_id: Optional[int] = None
    user_id: int
    exercise_id: int
    exercise_name: str
    exercise_description: Optional[str] = None
    sets: int
    reps: int
    date: date
    duration: int
    notes: Optional[str] = None

    class Config:
        from_attributes = True