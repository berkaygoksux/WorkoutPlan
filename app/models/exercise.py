from pydantic import BaseModel

class Exercise(BaseModel):
    exercise_id: int
    name: str
    description: str
    muscle_group: str
