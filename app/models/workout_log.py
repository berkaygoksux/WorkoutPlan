from pydantic import BaseModel
from datetime import date
from typing import Optional

class WorkoutLog(BaseModel):
    log_id: Optional[int] = None
    user_id: int
    exercise_id: int
    exercise_name: str
    exercise_description: str
    sets: int
    reps: int
    date: date
    duration: int
    notes: str = ""

    class Config:
        from_attributes = True