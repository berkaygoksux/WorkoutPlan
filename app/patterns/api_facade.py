from fastapi import FastAPI
from app.controllers import user_controller, workout_controller, auth_controller, workout_log_controller
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ApiFacade:
    def __init__(self, app: FastAPI):
        self.app = app

    def register_controllers(self):
        logger.info("Registering controllers")
        self.app.include_router(auth_controller.router, prefix="/auth", tags=["Auth"])
        self.app.include_router(user_controller.router, prefix="/user", tags=["User"])
        self.app.include_router(workout_controller.router, prefix="/workout", tags=["Workout"])
        self.app.include_router(workout_log_controller.router, prefix="/workout", tags=["WorkoutLog"])
        logger.info("Controllers registered successfully")