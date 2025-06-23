from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.workout_log import WorkoutLog, WorkoutLogCreate
from app.services.workout_log_service import WorkoutLogService
from app.controllers.auth_controller import get_current_user
from app.models.user import UserPublic
from sqlalchemy.orm import Session
from app.database import get_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/logs", response_model=WorkoutLog)
async def create_workout_log(
    log: WorkoutLogCreate,
    current_user: UserPublic = Depends(get_current_user),
    log_service: WorkoutLogService = Depends(),
    db: Session = Depends(get_db)
):
    logger.info(f"Creating workout log for user: {current_user.user_id}")
    try:
        new_log = WorkoutLog(
            user_id=current_user.user_id,
            exercise_id=log.exercise_id,
            exercise_name=log.exercise_name,
            exercise_description=log.exercise_description,
            sets=log.sets,
            reps=log.reps,
            date=log.date,
            duration=log.duration,
            notes=log.notes
        )
        created_log = log_service.create_log(new_log, db)
        return created_log
    except Exception as e:
        logger.error(f"Error creating workout log: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create log: {str(e)}")

@router.get("/logs", response_model=List[WorkoutLog])
async def get_workout_logs(
    current_user: UserPublic = Depends(get_current_user),
    log_service: WorkoutLogService = Depends(),
    db: Session = Depends(get_db)
):
    logger.info(f"Fetching workout logs for user: {current_user.user_id}")
    try:
        if current_user.role == "trainer":
            return log_service.get_all_logs(db)
        return log_service.get_logs_by_user(current_user.user_id, db)
    except Exception as e:
        logger.error(f"Error fetching workout logs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch logs: {str(e)}")

@router.get("/logs/{log_id}", response_model=WorkoutLog)
async def get_workout_log(
    log_id: int,
    current_user: UserPublic = Depends(get_current_user),
    log_service: WorkoutLogService = Depends(),
    db: Session = Depends(get_db)
):
    logger.info(f"Fetching workout log ID: {log_id}")
    try:
        log = log_service.get_log_by_id(log_id, db)
        if not log:
            raise HTTPException(status_code=404, detail="Log not found")
        if current_user.role != "trainer" and current_user.user_id != log.user_id:
            raise HTTPException(status_code=403, detail="You can only access your own logs")
        return log
    except Exception as e:
        logger.error(f"Error fetching workout log: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch log: {str(e)}")

@router.put("/logs/{log_id}", response_model=WorkoutLog)
async def update_workout_log(
    log_id: int,
    log_data: WorkoutLogCreate,
    current_user: UserPublic = Depends(get_current_user),
    log_service: WorkoutLogService = Depends(),
    db: Session = Depends(get_db)
):
    logger.info(f"Updating workout log ID: {log_id}")
    try:
        log = log_service.get_log_by_id(log_id, db)
        if not log:
            raise HTTPException(status_code=404, detail="Log not found")
        if current_user.role != "trainer" and current_user.user_id != log.user_id:
            raise HTTPException(status_code=403, detail="You can only update your own logs")

        updated_log = WorkoutLog(
            log_id=log_id,
            user_id=log.user_id,
            exercise_id=log_data.exercise_id,
            exercise_name=log_data.exercise_name,
            exercise_description=log_data.exercise_description,
            sets=log_data.sets,
            reps=log_data.reps,
            date=log_data.date,
            duration=log_data.duration,
            notes=log_data.notes
        )
        updated_log = log_service.update_log(updated_log, db)
        return updated_log
    except Exception as e:
        logger.error(f"Error updating workout log: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update log: {str(e)}")

@router.delete("/logs/{log_id}")
async def delete_workout_log(
    log_id: int,
    current_user: UserPublic = Depends(get_current_user),
    log_service: WorkoutLogService = Depends(),
    db: Session = Depends(get_db)
):
    logger.info(f"Deleting workout log ID: {log_id}")
    try:
        log = log_service.get_log_by_id(log_id, db)
        if not log:
            raise HTTPException(status_code=404, detail="Log not found")
        if current_user.role != "trainer" and current_user.user_id != log.user_id:
            raise HTTPException(status_code=403, detail="You can only delete your own logs")
        if not log_service.delete_log(log_id, db):
            raise HTTPException(status_code=404, detail="Log not found")
        return {"message": "Workout log deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting workout log: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete log: {str(e)}")