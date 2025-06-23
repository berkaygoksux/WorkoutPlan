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
    logger.info(f"Creating exercise: {exercise_data.name}")
    try:
        exercise = ExerciseFactory.create(
            exercise_type=exercise_data.exercise_type,
            exercise_id=0,
            name=exercise_data.name,
            description=exercise_data.description,
            muscle_group=exercise_data.muscle_group
        )
        created_exercise = exercise_service.create_exercise(exercise, db)
        logger.info(f"Exercise created: ID {created_exercise.exercise_id}, Name {created_exercise.name}")
        return created_exercise
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error creating exercise: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create exercise: {str(e)}")

@router.post("/plans", response_model=WorkoutPlan)
async def create_workout_plan(
    plan_data: WorkoutPlanCreate,
    current_user: UserPublic = Depends(get_current_user),
    plan_service: WorkoutPlanService = Depends(),
    exercise_service: ExerciseService = Depends(),
    user_service: UserService = Depends(),
    db: Session = Depends(get_db)
):
    logger.info(f"Creating workout plan for user: {current_user.user_id}")
    try:
        for exercise in plan_data.exercises:
            if not exercise_service.get_exercise_by_id(exercise.exercise_id, db):
                raise HTTPException(status_code=400, detail=f"Exercise ID {exercise.exercise_id} not found")

        target_user_id = plan_data.user_id if plan_data.user_id else current_user.user_id

        if current_user.role == "trainer":
            if target_user_id != current_user.user_id:
                target_user = user_service.get_user_by_id(target_user_id, db)
                if not target_user:
                    raise HTTPException(status_code=404, detail="Target user not found")
        else:
            if plan_data.user_id and plan_data.user_id != current_user.user_id:
                raise HTTPException(status_code=403, detail="You can only create plans for yourself")
            target_user_id = current_user.user_id

        created_plan = plan_service.create_plan(plan_data, target_user_id, db)
        logger.info(f"Plan created: Plan ID {created_plan.plan_id}, User ID {created_plan.user_id}")
        return created_plan
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error creating workout plan: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create plan: {str(e)}")

@router.get("/exercises", response_model=List[Exercise])
async def get_exercises(
    current_user: UserPublic = Depends(get_current_user),
    exercise_service: ExerciseService = Depends(),
    db: Session = Depends(get_db)
):
    logger.info(f"{current_user.email} is listing exercises")
    try:
        exercises = exercise_service.get_all_exercises(db)
        logger.info(f"Fetched {len(exercises)} exercises")
        return exercises
    except Exception as e:
        logger.error(f"Error fetching exercises: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch exercises: {str(e)}")

@router.get("/plans", response_model=List[WorkoutPlan])
async def get_workout_plans(
    current_user: UserPublic = Depends(get_current_user),
    plan_service: WorkoutPlanService = Depends(),
    db: Session = Depends(get_db)
):
    logger.info(f"Plan list requested by: {current_user.email}")
    try:
        if current_user.role == "trainer":
            plans = plan_service.get_all_plans(db)
        else:
            plans = plan_service.get_plans_by_user(current_user.user_id, db)
        logger.info(f"Fetched {len(plans)} plans")
        return plans
    except Exception as e:
        logger.error(f"Error fetching workout plans: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch plans: {str(e)}")

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
    logger.info(f"Updating exercise ID: {exercise_id}")
    try:
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
        logger.info(f"Exercise updated: ID {exercise_id}")
        return updated_exercise
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error updating exercise: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update exercise: {str(e)}")

@router.delete("/exercises/{exercise_id}")
async def delete_exercise(
    exercise_id: int,
    current_user: UserPublic = Depends(get_current_user),
    exercise_service: ExerciseService = Depends(),
    db: Session = Depends(get_db)
):
    if current_user.role != "trainer":
        raise HTTPException(status_code=403, detail="Only trainers can delete exercises")
    logger.info(f"Deleting exercise ID: {exercise_id}")
    try:
        if not exercise_service.delete_exercise(exercise_id, db):
            raise HTTPException(status_code=404, detail="Exercise not found")
        logger.info(f"Exercise deleted: ID {exercise_id}")
        return {"message": "Exercise deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error deleting exercise: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete exercise: {str(e)}")

@router.put("/plans/{plan_id}", response_model=WorkoutPlan)
async def update_workout_plan(
    plan_id: int,
    plan_data: WorkoutPlanCreate,
    current_user: UserPublic = Depends(get_current_user),
    plan_service: WorkoutPlanService = Depends(),
    exercise_service: ExerciseService = Depends(),
    db: Session = Depends(get_db)
):
    logger.info(f"Updating workout plan ID: {plan_id}")
    try:
        existing_plan = plan_service.get_plan_by_id(plan_id, db)
        if not existing_plan:
            raise HTTPException(status_code=404, detail="Plan not found")
        if current_user.role != "trainer" and existing_plan.user_id != current_user.user_id:
            raise HTTPException(status_code=403, detail="You can only update your own plans")

        for exercise in plan_data.exercises:
            if not exercise_service.get_exercise_by_id(exercise.exercise_id, db):
                raise HTTPException(status_code=400, detail=f"Exercise ID {exercise.exercise_id} not found")

        updated_plan = WorkoutPlan(
            plan_id=plan_id,
            user_id=existing_plan.user_id,
            title=plan_data.title,
            level=plan_data.level,
            exercises=plan_data.exercises,
            start_date=plan_data.start_date,
            end_date=plan_data.end_date,
            owner_name=existing_plan.owner_name
        )
        updated_plan = plan_service.update_plan(updated_plan, db)
        logger.info(f"Plan updated: Plan ID {plan_id}")
        return updated_plan
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error updating workout plan: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update plan: {str(e)}")

@router.delete("/plans/{plan_id}")
async def delete_workout_plan(
    plan_id: int,
    current_user: UserPublic = Depends(get_current_user),
    plan_service: WorkoutPlanService = Depends(),
    db: Session = Depends(get_db)
):
    logger.info(f"Deleting workout plan ID: {plan_id}")
    try:
        existing_plan = plan_service.get_plan_by_id(plan_id, db)
        if not existing_plan:
            raise HTTPException(status_code=404, detail="Plan not found")
        if current_user.role != "trainer" and existing_plan.user_id != current_user.user_id:
            raise HTTPException(status_code=403, detail="You can only delete your own plans")

        if not plan_service.delete_plan(plan_id, db):
            raise HTTPException(status_code=404, detail="Plan not found")
        logger.info(f"Plan deleted: Plan ID {plan_id}")
        return {"message": "Plan deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error deleting workout plan: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete plan: {str(e)}")