import logging
from fastapi import FastAPI
from dotenv import load_dotenv
from app.patterns.api_facade import ApiFacade

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
app = FastAPI()


api_facade = ApiFacade(app)
api_facade.register_controllers()

@app.get("/")
def root():
    logger.info("Root endpoint called.")
    return {"message": "Welcome to the GymGuider API!"}