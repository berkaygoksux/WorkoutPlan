from pydantic import BaseModel
from datetime import date

class WorkoutLog(BaseModel):
    log_id: int
    user_id: int
    exercise_id: int
    date: date
    duration: int  # dakika cinsinden
    notes: str = ""
