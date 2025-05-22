from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.workout_log import WorkoutLog
from app.models.workout_plan import WorkoutPlan
from app.database import WorkoutLogDB, ExerciseDB
from app.patterns.observers import EventManager, TrainerNotifier

class WorkoutLogService:
    def __init__(self):
        self.event_manager = EventManager()
        self.event_manager.subscribe(TrainerNotifier())

    def create_log(self, log: WorkoutLog, db: Session) -> WorkoutLog:
        db_log = WorkoutLogDB(**log.model_dump(exclude={"log_id"}))
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        self.event_manager.notify("log_created", {"log_id": db_log.log_id, "user_id": db_log.user_id})
        return WorkoutLog.from_orm(db_log)

    def create_logs_from_plan(self, plan: WorkoutPlan, db: Session) -> List[WorkoutLog]:
        logs = []
        duration_days = (plan.end_date - plan.start_date).days

        for exercise_in_plan in plan.exercises:
            exercise = db.query(ExerciseDB).filter(ExerciseDB.exercise_id == exercise_in_plan.exercise_id).first()
            if not exercise:
                raise ValueError(f"Excercise ID {exercise_in_plan.exercise_id} not found.")

            log = WorkoutLog(
                user_id=plan.user_id,
                exercise_id=exercise_in_plan.exercise_id,
                exercise_name=exercise.name,
                exercise_description=exercise.description,
                sets=exercise_in_plan.sets,
                reps=exercise_in_plan.reps,
                date=plan.start_date,
                duration=duration_days,
                notes=plan.title
            )
            db_log = self.create_log(log, db)
            logs.append(db_log)

        return logs

    def get_log_by_id(self, log_id: int, db: Session) -> Optional[WorkoutLog]:
        db_log = db.query(WorkoutLogDB).filter(WorkoutLogDB.log_id == log_id).first()
        return WorkoutLog.from_orm(db_log) if db_log else None

    def get_logs_by_user(self, user_id: int, db: Session) -> List[WorkoutLog]:
        db_logs = db.query(WorkoutLogDB).filter(WorkoutLogDB.user_id == user_id).all()
        return [WorkoutLog.from_orm(log) for log in db_logs]

    def get_all_logs(self, db: Session) -> List[WorkoutLog]:
        db_logs = db.query(WorkoutLogDB).all()
        return [WorkoutLog.from_orm(log) for log in db_logs]

    def update_log(self, log_id: int, db: Session, duration: Optional[int] = None, notes: Optional[str] = None) -> Optional[WorkoutLog]:
        db_log = db.query(WorkoutLogDB).filter(WorkoutLogDB.log_id == log_id).first()
        if not db_log:
            return None
        if duration:
            db_log.duration = duration
        if notes:
            db_log.notes = notes
        db.commit()
        db.refresh(db_log)
        return WorkoutLog.from_orm(db_log)

    def delete_log(self, log_id: int, db: Session) -> bool:
        db_log = db.query(WorkoutLogDB).filter(WorkoutLogDB.log_id == log_id).first()
        if not db_log:
            return False
        db.delete(db_log)
        db.commit()
        return True