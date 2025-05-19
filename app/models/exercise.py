from pydantic import BaseModel, Field
from typing import Optional

class ExerciseCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Name of the exercise")
    description: str = Field(..., min_length=1, max_length=500, description="Description of the exercise")
    muscle_group: str = Field(..., min_length=1, max_length=50, description="Target muscle group")
    exercise_type: str = Field(..., description="cardio/strength/flexibility")

class Exercise(BaseModel):
    exercise_id: Optional[int] = None
    name: str
    description: str
    muscle_group: str
    exercise_type: str

    class Config:
        from_attributes = True
