from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.user import UserPublic
from app.services.user_service import UserService
from app.controllers.auth_controller import get_current_user
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[UserPublic])
async def get_users(
    current_user: UserPublic = Depends(get_current_user),
    user_service: UserService = Depends(),
    db: Session = Depends(get_db)
):

    if current_user.role != "trainer":
        raise HTTPException(status_code=403, detail="Trainer privileges required")
    return user_service.get_all_users(db)

@router.get("/{user_id}", response_model=UserPublic)
async def get_user(
    user_id: int,
    current_user: UserPublic = Depends(get_current_user),
    user_service: UserService = Depends(),
    db: Session = Depends(get_db)
):

    if current_user.role != "trainer" and current_user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied: you can only access your own data or you must be a trainer")
    user = user_service.get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserPublic)
async def update_user(
    user_id: int,
    name: str = None,
    email: str = None,
    current_user: UserPublic = Depends(get_current_user),
    user_service: UserService = Depends(),
    db: Session = Depends(get_db)
):

    if current_user.role != "trainer" and current_user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied: you can only update your own data")
    user = user_service.update_user(user_id, db, name, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user: UserPublic = Depends(get_current_user),
    user_service: UserService = Depends(),
    db: Session = Depends(get_db)
):

    if current_user.role != "trainer" and current_user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied: you can only delete your own account")
    if not user_service.delete_user(user_id, db):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
