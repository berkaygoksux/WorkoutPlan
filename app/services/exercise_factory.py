from app.models.exercise import Exercise
from typing import Dict, Callable

class ExerciseFactory:
    _creators: Dict[str, Callable[..., Exercise]] = {}

    @classmethod
    def register_type(cls, exercise_type: str, creator: Callable[..., Exercise]):
        cls._creators[exercise_type.lower()] = creator

    @classmethod
    def create(cls, exercise_type: str, exercise_id: int, name: str, description: str, muscle_group: str) -> Exercise:
        creator = cls._creators.get(exercise_type.lower())
        if not creator:
            raise ValueError(f"Invalid exercise type: {exercise_type}")
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


ExerciseFactory.register_type("cardio", create_cardio_exercise)
ExerciseFactory.register_type("strength", create_strength_exercise)