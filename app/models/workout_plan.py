from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class ExerciseInPlan(BaseModel):
    exercise_id: int = Field(..., description="Database ID of the exercise")
    sets: int = Field(..., gt=0, description="Number of sets")
    reps: int = Field(..., gt=0, description="Number of repetitions")
    rest_seconds: int = Field(30, description="Rest duration (seconds)")

class WorkoutPlanCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    level: str = Field("beginner", description="beginner/intermediate/advanced")
    exercises: List[ExerciseInPlan]
    start_date: date
    end_date: date
    user_id: Optional[int] = None

class WorkoutPlan(WorkoutPlanCreate):
    plan_id: Optional[int] = None
    user_id: int

    class Config:
        from_attributes = True
