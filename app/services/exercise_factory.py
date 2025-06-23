from app.models.exercise import Exercise
from typing import Dict, Callable
from fastapi import HTTPException
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExerciseFactory:
    _creators: Dict[str, Callable[..., Exercise]] = {}

    @classmethod
    def register_type(cls, exercise_type: str, creator: Callable[..., Exercise]):
        cls._creators[exercise_type.lower()] = creator

    @classmethod
    def create(cls, exercise_type: str, exercise_id: int, name: str, description: str, muscle_group: str) -> Exercise:
        creator = cls._creators.get(exercise_type.lower())
        if not creator:
            logger.error(f"Invalid exercise type: {exercise_type}")
            raise HTTPException(
                status_code=400,
                detail=f"Invalid exercise type: {exercise_type}. Valid types: {list(cls._creators.keys())}"
            )
        logger.info(f"Creating exercise: {name} with type {exercise_type}")
        return creator(exercise_id=exercise_id, name=name, description=description, muscle_group=muscle_group)

def create_cardio_exercise(exercise_id: int, name: str, description: str, muscle_group: str) -> Exercise:
    return Exercise(
        exercise_id=exercise_id,
        name=name,
        description=description,
        muscle_group=muscle_group,
        exercise_type="cardio"
    )

def create_strength_exercise(exercise_id: int, name: str, description: str, muscle_group: str) -> Exercise:
    return Exercise(
        exercise_id=exercise_id,
        name=name,
        description=description,
        muscle_group=muscle_group,
        exercise_type="strength"
    )

def create_flexibility_exercise(exercise_id: int, name: str, description: str, muscle_group: str) -> Exercise:
    return Exercise(
        exercise_id=exercise_id,
        name=name,
        description=description,
        muscle_group=muscle_group,
        exercise_type="flexibility"
    )

ExerciseFactory.register_type("cardio", create_cardio_exercise)
ExerciseFactory.register_type("strength", create_strength_exercise)
ExerciseFactory.register_type("flexibility", create_flexibility_exercise)