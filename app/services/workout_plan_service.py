from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.workout_plan import WorkoutPlan
from app.database import WorkoutPlanDB
from app.patterns.observers import EventManager, TrainerNotifier
from app.services.workout_log_service import WorkoutLogService
import json

class WorkoutPlanService:
    def __init__(self):
        self.event_manager = EventManager()
        self.event_manager.subscribe(TrainerNotifier())

    def create_plan(self, plan: WorkoutPlan, db: Session) -> WorkoutPlan:

        plan_dict = plan.model_dump(exclude={"plan_id"})
        plan_dict["exercises"] = json.dumps(plan_dict["exercises"])

        db_plan = WorkoutPlanDB(**plan_dict)
        db.add(db_plan)
        db.commit()
        db.refresh(db_plan)


        created_plan = WorkoutPlan(
            plan_id=db_plan.plan_id,
            user_id=db_plan.user_id,
            title=db_plan.title,
            level=db_plan.level,
            exercises=json.loads(db_plan.exercises),
            start_date=db_plan.start_date,
            end_date=db_plan.end_date
        )


        self.event_manager.notify("plan_created", {
            "plan_id": created_plan.plan_id,
            "user_id": created_plan.user_id
        })


        log_service = WorkoutLogService()
        log_service.create_logs_from_plan(created_plan, db)

        return created_plan

    def get_plan_by_id(self, plan_id: int, db: Session) -> Optional[WorkoutPlan]:
        db_plan = db.query(WorkoutPlanDB).filter(WorkoutPlanDB.plan_id == plan_id).first()
        if not db_plan:
            return None
        return WorkoutPlan(
            plan_id=db_plan.plan_id,
            user_id=db_plan.user_id,
            title=db_plan.title,
            level=db_plan.level,
            exercises=json.loads(db_plan.exercises),
            start_date=db_plan.start_date,
            end_date=db_plan.end_date
        )

    def get_plans_by_user(self, user_id: int, db: Session) -> List[WorkoutPlan]:
        db_plans = db.query(WorkoutPlanDB).filter(WorkoutPlanDB.user_id == user_id).all()
        return [
            WorkoutPlan(
                plan_id=plan.plan_id,
                user_id=plan.user_id,
                title=plan.title,
                level=plan.level,
                exercises=json.loads(plan.exercises),
                start_date=plan.start_date,
                end_date=plan.end_date
            ) for plan in db_plans
        ]

    def get_all_plans(self, db: Session) -> List[WorkoutPlan]:
        db_plans = db.query(WorkoutPlanDB).all()
        return [
            WorkoutPlan(
                plan_id=plan.plan_id,
                user_id=plan.user_id,
                title=plan.title,
                level=plan.level,
                exercises=json.loads(plan.exercises),
                start_date=plan.start_date,
                end_date=plan.end_date
            ) for plan in db_plans
        ]

    def update_plan(self, plan: WorkoutPlan, db: Session) -> WorkoutPlan:
        db_plan = db.query(WorkoutPlanDB).filter(WorkoutPlanDB.plan_id == plan.plan_id).first()
        if not db_plan:
            raise HTTPException(status_code=404, detail="Plan not found.")


        db_plan.title = plan.title
        db_plan.level = plan.level

        db_plan.exercises = json.dumps([exercise.model_dump() for exercise in plan.exercises])
        db_plan.start_date = plan.start_date
        db_plan.end_date = plan.end_date

        db.commit()
        db.refresh(db_plan)


        return WorkoutPlan(
            plan_id=db_plan.plan_id,
            user_id=db_plan.user_id,
            title=db_plan.title,
            level=db_plan.level,
            exercises=json.loads(db_plan.exercises),
            start_date=db_plan.start_date,
            end_date=db_plan.end_date
        )

    def delete_plan(self, plan_id: int, db: Session) -> bool:
        db_plan = db.query(WorkoutPlanDB).filter(WorkoutPlanDB.plan_id == plan_id).first()
        if not db_plan:
            return False

        db.delete(db_plan)
        db.commit()
        return True