import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.user import UserInDB, UserPublic
from app.database import UserDB
from app.patterns.observers import EventManager, TrainerNotifier

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserService:
    def __init__(self):
        self.event_manager = EventManager()
        self.event_manager.subscribe(TrainerNotifier())

    def create_user(self, user: UserInDB, db: Session) -> UserPublic:
        logger.info(f"Creating user: {user.email}")
        if user.role not in ["user", "trainer"]:
            logger.warning(f"Invalid role: {user.role}")
            raise ValueError("Invalid role: must be either 'user' or 'trainer'")
        try:
            # Change the 'password' field to 'password_hash'
            user_data = user.model_dump(exclude={"user_id"})
            user_data["password_hash"] = user_data.pop("password")

            db_user = UserDB(**user_data)
            db.add(db_user)
            logger.debug("User added to database (before commit).")
            db.commit()
            logger.info(f"Commit successful: {user.email}")
            db.refresh(db_user)
            logger.info(f"User saved to database: {db_user.email}")
            self.event_manager.notify("user_created", {"email": db_user.email})
            return UserPublic.from_orm(db_user)
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            db.rollback()
            logger.info("Rollback performed.")
            raise

    def get_user_by_id(self, user_id: int, db: Session) -> Optional[UserPublic]:
        db_user = db.query(UserDB).filter(UserDB.user_id == user_id).first()
        return UserPublic.from_orm(db_user) if db_user else None

    def get_user_by_email(self, email: str, db: Session) -> Optional[UserInDB]:
        db_user = db.query(UserDB).filter(UserDB.email == email).first()
        if not db_user:
            return None
        return UserInDB(
            user_id=db_user.user_id,
            name=db_user.name,
            email=db_user.email,
            password=db_user.password_hash,
            role=db_user.role
        )

    def get_all_users(self, db: Session) -> List[UserPublic]:
        db_users = db.query(UserDB).all()
        return [UserPublic.from_orm(user) for user in db_users]

    def update_user(self, user_id: int, db: Session, name: Optional[str] = None, email: Optional[str] = None) -> Optional[UserPublic]:
        db_user = db.query(UserDB).filter(UserDB.user_id == user_id).first()
        if not db_user:
            return None
        if name:
            db_user.name = name
        if email:
            db_user.email = email
        db.commit()
        db.refresh(db_user)
        return UserPublic.from_orm(db_user)

    def delete_user(self, user_id: int, db: Session) -> bool:
        db_user = db.query(UserDB).filter(UserDB.user_id == user_id).first()
        if not db_user:
            return False
        db.delete(db_user)
        db.commit()
        return True
