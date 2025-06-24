from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.workout_log import WorkoutLog, WorkoutLogCreate
from app.database import WorkoutLogDB, ExerciseDB
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkoutLogService:
    def create_log(self, log: WorkoutLog, db: Session) -> WorkoutLog:
        try:
            db_exercise = db.query(ExerciseDB).filter(ExerciseDB.exercise_id == log.exercise_id).first()
            if not db_exercise:
                logger.error(f"Exercise ID {log.exercise_id} not found")
                raise HTTPException(status_code=400, detail=f"Exercise ID {log.exercise_id} not found")

            if log.exercise_name != db_exercise.name:
                logger.warning(f"Exercise name mismatch: provided '{log.exercise_name}', expected '{db_exercise.name}'")
                log.exercise_name = db_exercise.name

            db_log = WorkoutLogDB(
                user_id=log.user_id,
                exercise_id=log.exercise_id,
                exercise_name=log.exercise_name,
                exercise_description=log.exercise_description,
                sets=log.sets,
                reps=log.reps,
                date=log.date,
                duration=log.duration,
                notes=log.notes
            )
            db.add(db_log)
            db.commit()
            db.refresh(db_log)

            logger.info(f"Workout log created: Log ID {db_log.log_id}")
            return WorkoutLog(
                log_id=db_log.log_id,
                user_id=db_log.user_id,
                exercise_id=db_log.exercise_id,
                exercise_name=db_log.exercise_name,
                exercise_description=db_log.exercise_description,
                sets=db_log.sets,
                reps=db_log.reps,
                date=db_log.date,
                duration=db_log.duration,
                notes=db_log.notes
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Error creating log: {str(e)}")
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error creating log: {str(e)}")

    def get_log_by_id(self, log_id: int, db: Session) -> Optional[WorkoutLog]:
        try:
            db_log = db.query(WorkoutLogDB).filter(WorkoutLogDB.log_id == log_id).first()
            if not db_log:
                logger.info(f"Log ID {log_id} not found")
                return None
            return WorkoutLog(
                log_id=db_log.log_id,
                user_id=db_log.user_id,
                exercise_id=db_log.exercise_id,
                exercise_name=db_log.exercise_name,
                exercise_description=db_log.exercise_description,
                sets=db_log.sets,
                reps=db_log.reps,
                date=db_log.date,
                duration=db_log.duration,
                notes=db_log.notes
            )
        except Exception as e:
            logger.error(f"Error fetching log {log_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error fetching log: {str(e)}")

    def get_logs_by_user(self, user_id: int, db: Session) -> List[WorkoutLog]:
        try:
            db_logs = db.query(WorkoutLogDB).filter(WorkoutLogDB.user_id == user_id).all()
            logs = [
                WorkoutLog(
                    log_id=log.log_id,
                    user_id=log.user_id,
                    exercise_id=log.exercise_id,
                    exercise_name=log.exercise_name,
                    exercise_description=log.exercise_description,
                    sets=log.sets,
                    reps=log.reps,
                    date=log.date,
                    duration=log.duration,
                    notes=log.notes
                ) for log in db_logs
            ]
            logger.info(f"Fetched {len(logs)} logs for user {user_id}")
            return logs
        except Exception as e:
            logger.error(f"Error fetching logs for user {user_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error fetching logs: {str(e)}")

    def get_all_logs(self, db: Session) -> List[WorkoutLog]:
        try:
            db_logs = db.query(WorkoutLogDB).all()
            logs = [
                WorkoutLog(
                    log_id=log.log_id,
                    user_id=log.user_id,
                    exercise_id=log.exercise_id,
                    exercise_name=log.exercise_name,
                    exercise_description=log.exercise_description,
                    sets=log.sets,
                    reps=log.reps,
                    date=log.date,
                    duration=log.duration,
                    notes=log.notes
                ) for log in db_logs
            ]
            logger.info(f"Fetched {len(logs)} logs")
            return logs
        except Exception as e:
            logger.error(f"Error fetching all logs: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error fetching all logs: {str(e)}")

    def update_log(self, log: WorkoutLog, db: Session) -> WorkoutLog:
        try:
            db_log = db.query(WorkoutLogDB).filter(WorkoutLogDB.log_id == log.log_id).first()
            if not db_log:
                logger.error(f"Log ID {log.log_id} not found")
                raise HTTPException(status_code=404, detail="Log not found")

            db_exercise = db.query(ExerciseDB).filter(ExerciseDB.exercise_id == log.exercise_id).first()
            if not db_exercise:
                logger.error(f"Exercise ID {log.exercise_id} not found")
                raise HTTPException(status_code=400, detail=f"Exercise ID {log.exercise_id} not found")

            if log.exercise_name != db_exercise.name:
                logger.warning(f"Exercise name mismatch: provided '{log.exercise_name}', expected '{db_exercise.name}'")
                log.exercise_name = db_exercise.name

            db_log.exercise_id = log.exercise_id
            db_log.exercise_name = log.exercise_name
            db_log.exercise_description = log.exercise_description
            db_log.sets = log.sets
            db_log.reps = log.reps
            db_log.date = log.date
            db_log.duration = log.duration
            db_log.notes = log.notes

            db.commit()
            db.refresh(db_log)

            logger.info(f"Workout log updated: Log ID {db_log.log_id}")
            return WorkoutLog(
                log_id=db_log.log_id,
                user_id=db_log.user_id,
                exercise_id=db_log.exercise_id,
                exercise_name=db_log.exercise_name,
                exercise_description=db_log.exercise_description,
                sets=db_log.sets,
                reps=db_log.reps,
                date=db_log.date,
                duration=db_log.duration,
                notes=db_log.notes
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Error updating log {log.log_id}: {str(e)}")
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error updating log: {str(e)}")

    def delete_log(self, log_id: int, db: Session) -> bool:
        try:
            db_log = db.query(WorkoutLogDB).filter(WorkoutLogDB.log_id == log_id).first()
            if not db_log:
                logger.error(f"Log ID {log_id} not found")
                return False
            db.delete(db_log)
            db.commit()
            logger.info(f"Workout log deleted: Log ID {log_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting log {log_id}: {str(e)}")
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error deleting log: {str(e)}")