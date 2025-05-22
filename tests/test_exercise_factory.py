from app.services.exercise_factory import ExerciseFactory

def test_create_cardio_exercise():
    exercise = ExerciseFactory.create(
        exercise_type="cardio",
        exercise_id=1,
        name="Running",
        description="Run fast",
        muscle_group="legs"
    )
    assert exercise.exercise_type == "cardio"
    assert exercise.name == "Running"