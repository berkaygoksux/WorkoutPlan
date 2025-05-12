from pydantic import BaseModel

class UserPublic(BaseModel):
    user_id: int
    name: str
    email: str

class UserInDB(UserPublic):
    password_hash: str
