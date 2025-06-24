from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from app.models.user import UserPublic, UserInDB
from app.services.user_service import UserService
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from app.database import get_db
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    logger.error("SECRET_KEY environment variable not found!")
    raise ValueError("SECRET_KEY environment variable not found!")
logger.info("SECRET_KEY loaded successfully")

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "user"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    logger.info(f"Creating token for: {data}")
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        logger.info("Token created successfully")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Failed to create token: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(),
    db: Session = Depends(get_db)
) -> UserPublic:
    logger.info("Verifying token")
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid token, please log in again.",
    )
    if not token:
        logger.warning("Token is missing")
        raise credentials_exception
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            logger.warning("Email missing in token payload")
            raise credentials_exception
        logger.info(f"Token decoded, email: {email}")
    except JWTError as e:
        logger.error(f"JWT error: {e}")
        raise credentials_exception
    user = user_service.get_user_by_email(email, db)
    if user is None:
        logger.warning(f"User not found: {email}")
        raise credentials_exception
    logger.info(f"User verified: {user.email}")
    return UserPublic.from_orm(user)

@router.post("/register", response_model=UserPublic)
def register_user(
    data: RegisterRequest,
    user_service: UserService = Depends(),
    db: Session = Depends(get_db)
):
    logger.info(f"Registration attempt: {data.email}")
    try:
        existing_user = user_service.get_user_by_email(data.email, db)
        if existing_user:
            logger.warning(f"Email already registered: {data.email}")
            raise HTTPException(status_code=400, detail="This email is already registered")
        if data.role not in ["user", "trainer"]:
            logger.warning(f"Invalid role: {data.role}")
            raise HTTPException(status_code=400, detail="Invalid role: must be 'user' or 'trainer'")
        hashed_password = pwd_context.hash(data.password)
        logger.debug("Password hashed")
        new_user = UserInDB(
            name=data.name,
            email=data.email,
            password=hashed_password,
            role=data.role
        )
        created_user = user_service.create_user(new_user, db)
        logger.info(f"User created: {created_user.email}")
        return created_user
    except Exception as e:
        logger.error(f"User creation error: {e}")
        raise HTTPException(status_code=500, detail=f"User could not be created: {str(e)}")

@router.post("/login", response_model=Token)
def login_user(
    data: LoginRequest,
    user_service: UserService = Depends(),
    db: Session = Depends(get_db)
):
    logger.info(f"Login attempt: {data.email}")
    try:
        user = user_service.get_user_by_email(data.email, db)
        if not user:
            logger.warning(f"User not found: {data.email}")
            raise HTTPException(status_code=401, detail="Invalid credentials")
        if not pwd_context.verify(data.password, user.password):
            logger.warning(f"Password verification failed for {data.email}")
            raise HTTPException(status_code=401, detail="Invalid credentials")
        access_token = create_access_token(data={"sub": user.email, "role": user.role})
        logger.info(f"Token created for {data.email}")
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")