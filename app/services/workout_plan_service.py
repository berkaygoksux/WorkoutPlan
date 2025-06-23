from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import join
from fastapi import HTTPException
from app.models.workout_plan import WorkoutPlan, WorkoutPlanCreate, PlanExercise
from app.models.workout_log import WorkoutLog, WorkoutLogCreate
from app.database import WorkoutPlanDB, ExerciseDB, UserDB
from app.services.workout_log_service import WorkoutLogService
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkoutPlanService:
    def create_plan(self, plan: WorkoutPlanCreate, user_id: int, db: Session) -> WorkoutPlan:
        try:

            exercises_with_names = []
            for exercise in plan.exercises:
                db_exercise = db.query(ExerciseDB).filter(ExerciseDB.exercise_id == exercise.exercise_id).first()
                if not db_exercise:
                    logger.error(f"Exercise ID {exercise.exercise_id} not found")
                    raise HTTPException(status_code=400, detail=f"Exercise ID {exercise.exercise_id} not found")
                exercises_with_names.append({
                    "exercise_id": exercise.exercise_id,
                    "name": db_exercise.name,
                    "sets": exercise.sets,
                    "reps": exercise.reps,
                    "rest_seconds": exercise.rest_seconds or 30
                })


            final_user_id = plan.user_id if plan.user_id else user_id


            db_plan = WorkoutPlanDB(
                user_id=final_user_id,
                title=plan.title,
                level=plan.level,
                exercises=json.dumps(exercises_with_names),
                start_date=plan.start_date,
                end_date=plan.end_date
            )
            db.add(db_plan)
            db.commit()
            db.refresh(db_plan)


            log_service = WorkoutLogService()
            for exercise in plan.exercises:
                db_exercise = db.query(ExerciseDB).filter(ExerciseDB.exercise_id == exercise.exercise_id).first()
                new_log = WorkoutLog(
                    user_id=final_user_id,
                    exercise_id=exercise.exercise_id,
                    exercise_name=db_exercise.name,
                    exercise_description=db_exercise.description,
                    sets=exercise.sets,
                    reps=exercise.reps,
                    date=plan.start_date,
                    duration=30,
                    notes=f"Auto-generated log for plan: {plan.title}"
                )
                created_log = log_service.create_log(new_log, db)
                logger.info(f"Auto-generated workout log: Log ID {created_log.log_id}, Exercise ID {exercise.exercise_id}, Plan ID {db_plan.plan_id}")


            db_user = db.query(UserDB).filter(UserDB.user_id == db_plan.user_id).first()
            owner_name = db_user.name if db_user else "Unknown User"

            logger.info(f"Plan created: Plan ID {db_plan.plan_id}, User ID {db_plan.user_id}")
            return WorkoutPlan(
                plan_id=db_plan.plan_id,
                user_id=db_plan.user_id,
                title=db_plan.title,
                level=db_plan.level,
                exercises=[
                    PlanExercise(
                        exercise_id=ex["exercise_id"],
                        name=ex["name"],
                        sets=ex["sets"],
                        reps=ex["reps"],
                        rest_seconds=ex["rest_seconds"]
                    ) for ex in json.loads(db_plan.exercises)
                ],
                start_date=db_plan.start_date,
                end_date=db_plan.end_date,
                owner_name=owner_name
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Error creating plan: {str(e)}")
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error creating plan: {str(e)}")

    def get_plan_by_id(self, plan_id: int, db: Session) -> Optional[WorkoutPlan]:
        try:
            db_plan = (
                db.query(WorkoutPlanDB, UserDB.name.label("owner_name"))
                .join(UserDB, WorkoutPlanDB.user_id == UserDB.user_id)
                .filter(WorkoutPlanDB.plan_id == plan_id)
                .first()
            )
            if not db_plan:
                logger.info(f"Plan ID {plan_id} not found")
                return None
            db_plan, owner_name = db_plan
            exercises = json.loads(db_plan.exercises) if db_plan.exercises else []
            return WorkoutPlan(
                plan_id=db_plan.plan_id,
                user_id=db_plan.user_id,
                title=db_plan.title,
                level=db_plan.level,
                exercises=[
                    PlanExercise(
                        exercise_id=ex["exercise_id"],
                        name=ex.get("name", "Unknown Exercise"),
                        sets=ex["sets"],
                        reps=ex["reps"],
                        rest_seconds=ex.get("rest_seconds", 30)
                    ) for ex in exercises
                ],
                start_date=db_plan.start_date,
                end_date=db_plan.end_date,
                owner_name=owner_name or "Unknown User"
            )
        except Exception as e:
            logger.error(f"Error fetching plan {plan_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error fetching plan: {str(e)}")

    def get_plans_by_user(self, user_id: int, db: Session) -> List[WorkoutPlan]:
        try:
            db_plans = (
                db.query(WorkoutPlanDB, UserDB.name.label("owner_name"))
                .join(UserDB, WorkoutPlanDB.user_id == UserDB.user_id)
                .filter(WorkoutPlanDB.user_id == user_id)
                .all()
            )
            plans = []
            for db_plan, owner_name in db_plans:
                exercises = json.loads(db_plan.exercises) if db_plan.exercises else []
                plans.append(
                    WorkoutPlan(
                        plan_id=db_plan.plan_id,
                        user_id=db_plan.user_id,
                        title=db_plan.title,
                        level=db_plan.level,
                        exercises=[
                            PlanExercise(
                                exercise_id=ex["exercise_id"],
                                name=ex.get("name", "Unknown Exercise"),
                                sets=ex["sets"],
                                reps=ex["reps"],
                                rest_seconds=ex.get("rest_seconds", 30)
                            ) for ex in exercises
                        ],
                        start_date=db_plan.start_date,
                        end_date=db_plan.end_date,
                        owner_name=owner_name or "Unknown User"
                    )
                )
            logger.info(f"Fetched {len(plans)} plans for user {user_id}")
            return plans
        except Exception as e:
            logger.error(f"Error fetching plans for user {user_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error fetching plans: {str(e)}")

    def get_all_plans(self, db: Session) -> List[WorkoutPlan]:
        try:
            db_plans = (
                db.query(WorkoutPlanDB, UserDB.name.label("owner_name"))
                .join(UserDB, WorkoutPlanDB.user_id == UserDB.user_id)
                .all()
            )
            plans = []
            for db_plan, owner_name in db_plans:
                exercises = json.loads(db_plan.exercises) if db_plan.exercises else []
                plans.append(
                    WorkoutPlan(
                        plan_id=db_plan.plan_id,
                        user_id=db_plan.user_id,
                        title=db_plan.title,
                        level=db_plan.level,
                        exercises=[
                            PlanExercise(
                                exercise_id=ex["exercise_id"],
                                name=ex.get("name", "Unknown Exercise"),
                                sets=ex["sets"],
                                reps=ex["reps"],
                                rest_seconds=ex.get("rest_seconds", 30)
                            ) for ex in exercises
                        ],
                        start_date=db_plan.start_date,
                        end_date=db_plan.end_date,
                        owner_name=owner_name or "Unknown User"
                    )
                )
            logger.info(f"Fetched {len(plans)} plans")
            return plans
        except Exception as e:
            logger.error(f"Error fetching all plans: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error fetching all plans: {str(e)}")

    def update_plan(self, plan: WorkoutPlan, db: Session) -> WorkoutPlan:
        try:
            db_plan = db.query(WorkoutPlanDB).filter(WorkoutPlanDB.plan_id == plan.plan_id).first()
            if not db_plan:
                logger.error(f"Plan ID {plan.plan_id} not found")
                raise HTTPException(status_code=404, detail="Plan not found")

            exercises_with_names = []
            for exercise in plan.exercises:
                db_exercise = db.query(ExerciseDB).filter(ExerciseDB.exercise_id == exercise.exercise_id).first()
                if not db_exercise:
                    logger.error(f"Exercise ID {exercise.exercise_id} not found")
                    raise HTTPException(status_code=400, detail=f"Exercise ID {exercise.exercise_id} not found")
                exercises_with_names.append({
                    "exercise_id": exercise.exercise_id,
                    "name": db_exercise.name,
                    "sets": exercise.sets,
                    "reps": exercise.reps,
                    "rest_seconds": exercise.rest_seconds or 30
                })

            db_plan.title = plan.title
            db_plan.level = plan.level
            db_plan.exercises = json.dumps(exercises_with_names)
            db_plan.start_date = plan.start_date
            db_plan.end_date = plan.end_date

            db.commit()
            db.refresh(db_plan)

            db_user = db.query(UserDB).filter(UserDB.user_id == db_plan.user_id).first()
            owner_name = db_user.name if db_user else "Unknown User"

            exercises = json.loads(db_plan.exercises) if db_plan.exercises else []
            logger.info(f"Plan updated: Plan ID {db_plan.plan_id}")
            return WorkoutPlan(
                plan_id=db_plan.plan_id,
                user_id=db_plan.user_id,
                title=db_plan.title,
                level=db_plan.level,
                exercises=[
                    PlanExercise(
                        exercise_id=ex["exercise_id"],
                        name=ex.get("name", "Unknown Exercise"),
                        sets=ex["sets"],
                        reps=ex["reps"],
                        rest_seconds=ex.get("rest_seconds", 30)
                    ) for ex in exercises
                ],
                start_date=db_plan.start_date,
                end_date=db_plan.end_date,
                owner_name=owner_name
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Error updating plan {plan.plan_id}: {str(e)}")
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error updating plan: {str(e)}")

    def delete_plan(self, plan_id: int, db: Session) -> bool:
        try:
            db_plan = db.query(WorkoutPlanDB).filter(WorkoutPlanDB.plan_id == plan_id).first()
            if not db_plan:
                logger.error(f"Plan ID {plan_id} not found")
                return False
            db.delete(db_plan)
            db.commit()
            logger.info(f"Plan deleted: Plan ID {plan_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting plan {plan_id}: {str(e)}")
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error deleting plan: {str(e)}")