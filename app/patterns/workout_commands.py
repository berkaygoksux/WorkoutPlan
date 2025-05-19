from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from app.models.workout_plan import WorkoutPlan
from app.services.workout_plan_service import WorkoutPlanService

class Command(ABC):
    @abstractmethod
    def execute(self, db: Session):
        pass

class CreateWorkoutPlanCommand(Command):
    def __init__(self, plan_service: WorkoutPlanService, plan: WorkoutPlan):
        self.plan_service = plan_service
        self.plan = plan

    def execute(self, db: Session) -> WorkoutPlan:
        return self.plan_service.create_plan(self.plan, db)