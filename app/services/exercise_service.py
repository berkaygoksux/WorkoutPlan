import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.exercise import Exercise
from app.database import ExerciseDB
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExerciseService:
    def get_exercise_by_id(self, exercise_id: int, db: Session) -> Optional[Exercise]:
        db_exercise = db.query(ExerciseDB).filter(ExerciseDB.exercise_id == exercise_id).first()
        if not db_exercise:
            return None
        return Exercise(
            exercise_id=db_exercise.exercise_id,
            name=db_exercise.name,
            description=db_exercise.description,
            muscle_group=db_exercise.muscle_group,
            exercise_type=db_exercise.exercise_type
        )

    def create_exercise(self, exercise: Exercise, db: Session) -> Exercise:
        logger.info(f"Creating exercise: {exercise.name}")
        try:
            db_exercise = ExerciseDB(
                name=exercise.name,
                description=exercise.description,
                muscle_group=exercise.muscle_group,
                exercise_type=exercise.exercise_type
            )
            db.add(db_exercise)
            db.commit()
            db.refresh(db_exercise)
            logger.info(f"Exercise successfully created: {db_exercise.name}, ID: {db_exercise.exercise_id}")
            return Exercise.from_orm(db_exercise)
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Database error: {e}")
            raise HTTPException(status_code=400, detail="An exercise with this name already exists")
        except Exception as e:
            db.rollback()
            logger.error(f"Exercise creation error: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to create exercise: {str(e)}")

    def get_all_exercises(self, db: Session) -> List[Exercise]:
        db_exercises = db.query(ExerciseDB).all()
        return [Exercise.from_orm(exercise) for exercise in db_exercises]

    def update_exercise(self, exercise: Exercise, db: Session) -> Optional[Exercise]:
        db_exercise = db.query(ExerciseDB).filter(ExerciseDB.exercise_id == exercise.exercise_id).first()
        if not db_exercise:
            return None

        db_exercise.name = exercise.name
        db_exercise.description = exercise.description
        db_exercise.muscle_group = exercise.muscle_group
        db_exercise.exercise_type = exercise.exercise_type

        db.commit()
        db.refresh(db_exercise)
        return Exercise.from_orm(db_exercise)

    def delete_exercise(self, exercise_id: int, db: Session) -> bool:
        db_exercise = db.query(ExerciseDB).filter(ExerciseDB.exercise_id == exercise_id).first()
        if not db_exercise:
            return False

        db.delete(db_exercise)
        db.commit()
        return True
