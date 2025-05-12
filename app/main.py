from fastapi import FastAPI
from app.controllers.user_controller import router as user_router
from app.controllers.workout_controller import router as workout_router
from app.controllers.auth_controller import router as auth_router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "GymGuider API'ye hoş geldiniz!"}

app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(workout_router, prefix="/workout", tags=["Workout"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
