from pydantic import BaseModel
from typing import List
from app.models.exercise import Exercise

class WorkoutPlan(BaseModel):
    plan_id: int
    user_id: int
    title: str
    exercises: List[Exercise]
