import logging
from fastapi import FastAPI
from dotenv import load_dotenv
from app.patterns.api_facade import ApiFacade
from fastapi.middleware.cors import CORSMiddleware
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:51611",
    os.getenv("FRONTEND_URL", "http://localhost:3001"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "Authorization"],
)

api_facade = ApiFacade(app)
api_facade.register_controllers()

@app.get("/")
def root():
    logger.info("Root endpoint called")
    return {"message": "Welcome to the WorkoutPlan API!"}