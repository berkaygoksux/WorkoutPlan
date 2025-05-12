from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.data_storage import users
from passlib.context import CryptContext
from app.models.user import UserPublic, UserInDB

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

@router.post("/register", response_model=UserPublic)
def register_user(data: RegisterRequest):
    if any(user.email == data.email for user in users):
        raise HTTPException(status_code=400, detail="Bu e-posta zaten kayıtlı.")

    hashed_password = pwd_context.hash(data.password)

    new_user = UserInDB(
        user_id=len(users) + 1,
        name=data.name,
        email=data.email,
        password_hash=hashed_password
    )

    users.append(new_user)

    #terminal üzerinde register olan kullanıcı bilgilerini görmek için
    print("Kayıtlı kullanıcılar:")
    for user in users:
        print(user)

    return UserPublic(
        user_id=new_user.user_id,
        name=new_user.name,
        email=new_user.email
    )

