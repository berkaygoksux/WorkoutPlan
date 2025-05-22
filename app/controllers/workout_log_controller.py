from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.workout_log import WorkoutLog
from app.services.workout_log_service import WorkoutLogService
from app.controllers.auth_controller import get_current_user
from app.models.user import UserPublic
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.post("/logs", response_model=WorkoutLog)
async def create_workout_log(log: WorkoutLog, current_user: UserPublic = Depends(get_current_user), log_service: WorkoutLogService = Depends(), db: Session = Depends(get_db)):
    if current_user.role != "trainer" and current_user.user_id != log.user_id:
        raise HTTPException(status_code=403, detail="You can only create your own logs")
    return log_service.create_log(log, db)

@router.get("/logs", response_model=List[WorkoutLog])
async def get_workout_logs(current_user: UserPublic = Depends(get_current_user), log_service: WorkoutLogService = Depends(), db: Session = Depends(get_db)):
    if current_user.role == "trainer":
        return log_service.get_all_logs(db)
    return log_service.get_logs_by_user(current_user.user_id, db)

@router.get("/logs/{log_id}", response_model=WorkoutLog)
async def get_workout_log(log_id: int, current_user: UserPublic = Depends(get_current_user), log_service: WorkoutLogService = Depends(), db: Session = Depends(get_db)):
    log = log_service.get_log_by_id(log_id, db)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    if current_user.role != "trainer" and current_user.user_id != log.user_id:
        raise HTTPException(status_code=403, detail="You can only access your own logs")
    return log

@router.put("/logs/{log_id}", response_model=WorkoutLog)
async def update_workout_log(log_id: int, duration: int = None, notes: str = None, current_user: UserPublic = Depends(get_current_user), log_service: WorkoutLogService = Depends(), db: Session = Depends(get_db)):
    log = log_service.get_log_by_id(log_id, db)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    if current_user.role != "trainer" and current_user.user_id != log.user_id:
        raise HTTPException(status_code=403, detail="You can only update your own logs")
    updated_log = log_service.update_log(log_id, db, duration, notes)
    if not updated_log:
        raise HTTPException(status_code=404, detail="Log not found")
    return updated_log

@router.delete("/logs/{log_id}")
async def delete_workout_log(log_id: int, current_user: UserPublic = Depends(get_current_user), log_service: WorkoutLogService = Depends(), db: Session = Depends(get_db)):
    log = log_service.get_log_by_id(log_id, db)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    if current_user.role != "trainer" and current_user.user_id != log.user_id:
        raise HTTPException(status_code=403, detail="You can only delete your own logs")
    if not log_service.delete_log(log_id, db):
        raise HTTPException(status_code=404, detail="Log not found")
    return {"message": "Log deleted"}
