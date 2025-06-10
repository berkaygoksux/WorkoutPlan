from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.exercise import Exercise, ExerciseCreate
from app.models.workout_plan import WorkoutPlan, WorkoutPlanCreate
from app.services.exercise_factory import ExerciseFactory
from app.services.exercise_service import ExerciseService
from app.services.workout_plan_service import WorkoutPlanService
from app.services.user_service import UserService  
from app.controllers.auth_controller import get_current_user
from app.models.user import UserPublic
from sqlalchemy.orm import Session
from app.database import get_db

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/exercises", response_model=Exercise)
async def create_exercise(
        exercise_data: ExerciseCreate,
        current_user: UserPublic = Depends(get_current_user),
        exercise_service: ExerciseService = Depends(),
        db: Session = Depends(get_db)
):
    if current_user.role != "trainer":
        raise HTTPException(status_code=403, detail="Only trainers can create exercises")


    exercise = ExerciseFactory.create(
        exercise_type=exercise_data.exercise_type,
        exercise_id=0,
        name=exercise_data.name,
        description=exercise_data.description,
        muscle_group=exercise_data.muscle_group
    )

    return exercise_service.create_exercise(exercise, db)


@router.post("/plans", response_model=WorkoutPlan)
async def create_workout_plan(
    plan_data: WorkoutPlanCreate,
    current_user: UserPublic = Depends(get_current_user),
    plan_service: WorkoutPlanService = Depends(),
    exercise_service: ExerciseService = Depends(),
    user_service: UserService = Depends(),
    db: Session = Depends(get_db)
):

    for exercise in plan_data.exercises:
        if not exercise_service.get_exercise_by_id(exercise.exercise_id, db):
            raise HTTPException(
                status_code=400,
                detail=f"Exercise ID {exercise.exercise_id} not found"
            )


    target_user_id = plan_data.user_id if plan_data.user_id else current_user.user_id

    if current_user.role == "trainer":

        if target_user_id != current_user.user_id:
            target_user = user_service.get_user_by_id(target_user_id, db)
            if not target_user:
                raise HTTPException(status_code=404, detail="Target user not found")
    else:

        if plan_data.user_id and plan_data.user_id != current_user.user_id:
            raise HTTPException(
                status_code=403,
                detail="You can only create plans for your own account"
            )
        target_user_id = current_user.user_id

    plan = WorkoutPlan(
        **plan_data.model_dump(exclude={"user_id"}),
        user_id=target_user_id
    )
    created_plan = plan_service.create_plan(plan, db)
    logger.info(f"Plan created: Plan ID {created_plan.plan_id}, User ID {created_plan.user_id}")
    return created_plan


@router.get("/exercises", response_model=List[Exercise])
async def get_exercises(
    current_user: UserPublic = Depends(get_current_user),
    exercise_service: ExerciseService = Depends(),
    db: Session = Depends(get_db)
):
    logger.info(f"{current_user.email} is listing exercises")
    return exercise_service.get_all_exercises(db)


@router.get("/plans", response_model=List[WorkoutPlan])
async def get_workout_plans(
    current_user: UserPublic = Depends(get_current_user),
    plan_service: WorkoutPlanService = Depends(),
    db: Session = Depends(get_db)
):
    logger.info(f"Plan list requested: {current_user.email}")
    if current_user.role == "trainer":
        return plan_service.get_all_plans(db)
    return plan_service.get_plans_by_user(current_user.user_id, db)


@router.put("/exercises/{exercise_id}", response_model=Exercise)
async def update_exercise(
        exercise_id: int,
        exercise_data: ExerciseCreate,
        current_user: UserPublic = Depends(get_current_user),
        exercise_service: ExerciseService = Depends(),
        db: Session = Depends(get_db)
):
    if current_user.role != "trainer":
        raise HTTPException(status_code=403, detail="Only trainers can update exercises")

    exercise = ExerciseFactory.create(
        exercise_type=exercise_data.exercise_type,
        exercise_id=exercise_id,
        name=exercise_data.name,
        description=exercise_data.description,
        muscle_group=exercise_data.muscle_group
    )

    updated_exercise = exercise_service.update_exercise(exercise, db)
    if not updated_exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return updated_exercise


@router.delete("/exercises/{exercise_id}")
async def delete_exercise(
        exercise_id: int,
        current_user: UserPublic = Depends(get_current_user),
        exercise_service: ExerciseService = Depends(),
        db: Session = Depends(get_db)
):
    if current_user.role != "trainer":
        raise HTTPException(status_code=403, detail="Only trainers can delete exercises")

    if not exercise_service.delete_exercise(exercise_id, db):
        raise HTTPException(status_code=404, detail="Exercise not found")
    return {"message": "Exercise deleted successfully"}



@router.put("/plans/{plan_id}", response_model=WorkoutPlan)
async def update_workout_plan(
    plan_id: int,
    plan_data: WorkoutPlanCreate,
    current_user: UserPublic = Depends(get_current_user),
    plan_service: WorkoutPlanService = Depends(),
    exercise_service: ExerciseService = Depends(),
    db: Session = Depends(get_db)
):
    if current_user.role != "trainer":
        raise HTTPException(status_code=403, detail="Only trainers can update plans")

    for exercise in plan_data.exercises:
        if not exercise_service.get_exercise_by_id(exercise.exercise_id, db):
            raise HTTPException(status_code=400, detail=f"Exercise ID {exercise.exercise_id} not found")

    existing_plan = plan_service.get_plan_by_id(plan_id, db)
    if not existing_plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    updated_plan = WorkoutPlan(
        plan_id=plan_id,
        user_id=existing_plan.user_id,
        title=plan_data.title,
        level=plan_data.level,
        exercises=plan_data.exercises,
        start_date=plan_data.start_date,
        end_date=plan_data.end_date
    )

    return plan_service.update_plan(updated_plan, db)


@router.delete("/plans/{plan_id}")
async def delete_workout_plan(
    plan_id: int,
    current_user: UserPublic = Depends(get_current_user),
    plan_service: WorkoutPlanService = Depends(),
    db: Session = Depends(get_db)
):
    if current_user.role != "trainer":
        raise HTTPException(status_code=403, detail="Only trainers can delete plans")

    if not plan_service.delete_plan(plan_id, db):
        raise HTTPException(status_code=404, detail="Plan not found")

    return {"message": "Plan deleted successfully"}
