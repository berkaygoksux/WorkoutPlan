from fastapi import APIRouter
from app.models.user import UserPublic
from app.services.data_storage import users

router = APIRouter()

@router.get("/", response_model=UserPublic)
def get_users():
    return UserPublic(
        user_id=users[0].user_id,
        name=users[0].name,
        email=users[0].email
    )
