import logging
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import pathlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///gymguider.db")

if DATABASE_URL.startswith("sqlite:///"):
    db_path = DATABASE_URL.replace("sqlite:///", "")
    absolute_path = str(pathlib.Path(db_path).resolve())
    DATABASE_URL = f"sqlite:///{absolute_path}"
logger.info(f"Database URL: {DATABASE_URL}")

try:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    logger.info("Database engine created.")
except Exception as e:
    logger.error(f"Database connection error: {e}")
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="user")

class ExerciseDB(Base):
    __tablename__ = "exercises"
    exercise_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    muscle_group = Column(String, nullable=False)
    exercise_type = Column(String, nullable=False)

class WorkoutPlanDB(Base):
    __tablename__ = "workout_plans"
    plan_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    title = Column(String, nullable=False)
    level = Column(String, default="beginner")
    exercises = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)

class WorkoutLogDB(Base):
    __tablename__ = "workout_logs"
    log_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.exercise_id"), nullable=False)
    exercise_name = Column(String, nullable=False)
    exercise_description = Column(String, nullable=True)  # Opsiyonel
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    duration = Column(Integer, nullable=False)
    notes = Column(String, nullable=True)

try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created or already exist.")
except Exception as e:
    logger.error(f"Table creation error: {e}")
    raise

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()
        logger.debug("Database session closed.")