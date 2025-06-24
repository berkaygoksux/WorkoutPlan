from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class PlanExercise(BaseModel):
    exercise_id: int
    name: Optional[str] = None
    sets: int
    reps: int
    rest_seconds: Optional[int] = 30

    class Config:
        from_attributes = True

class WorkoutPlanCreate(BaseModel):
    title: str
    level: str
    start_date: date
    end_date: date
    exercises: List[PlanExercise]
    user_id: Optional[int] = None

class WorkoutPlan(BaseModel):
    plan_id: Optional[int] = None
    user_id: int
    title: str
    level: str
    exercises: List[PlanExercise]
    start_date: date
    end_date: date
    owner_name: Optional[str] = None

    class Config:
        from_attributes = True