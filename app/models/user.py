from pydantic import BaseModel
from typing import Optional

class UserInDB(BaseModel):
    user_id: Optional[int] = None
    name: str
    email: str
    password: str
    role: str

    class Config:
        from_attributes = True

class UserPublic(BaseModel):
    user_id: Optional[int] = None
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True