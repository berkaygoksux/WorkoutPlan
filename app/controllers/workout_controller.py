from fastapi import APIRouter
from app.models.exercise import Exercise
from app.models.workout_plan import WorkoutPlan
from app.services.data_storage import exercises, workout_plans

router = APIRouter()
@router.get("/")
def get_users():
    return "workout page"

@router.get("/exercises", response_model=list[Exercise])
def get_exercises():
    return exercises

@router.get("/plans", response_model=list[WorkoutPlan])
def get_workout_plans():
    return workout_plans
