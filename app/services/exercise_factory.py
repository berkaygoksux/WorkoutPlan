from app.models.exercise import Exercise

class ExerciseFactory:
    @staticmethod
    def create(exercise_type, exercise_id, name, description, muscle_group):
        if exercise_type.lower() in ["cardio", "strength", "flexibility"]:
            return Exercise(
                exercise_id=exercise_id,
                name=name,
                description=description,
                muscle_group=muscle_group
            )
        else:
            raise ValueError(f"Invalid exercise type: {exercise_type}")
