from datetime import date
from app.models.user import UserInDB
from app.models.workout_log import WorkoutLog
from app.models.workout_plan import WorkoutPlan
from app.services.exercise_factory import ExerciseFactory

users = [
    UserInDB(
        user_id=1,
        name="Semih",
        email="semih@example.com",
        password_hash="hashedpass"
    )
]

exercises = [
    ExerciseFactory.create(
        exercise_type="cardio",
        exercise_id=1,
        name="Running",
        description="Run 30 mins",
        muscle_group="Legs"
    ),
    ExerciseFactory.create(
        exercise_type="strength",
        exercise_id=2,
        name="Bench Press",
        description="Chest workout",
        muscle_group="Chest"
    )
]

workout_plans = [
    WorkoutPlan(
        plan_id=1,
        user_id=1,
        title="Göğüs Günü",
        exercises=exercises[:1]  # İlk egzersizi eklemek için
    )
]

logs = [
    WorkoutLog(
        log_id=1,
        user_id=1,
        exercise_id=1,
        date=date.today(),
        duration=30,
        notes="İyi geçti"
    )
]