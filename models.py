from typing import Optional
from pydantic import BaseModel, EmailStr

# user models


class UserIn(BaseModel):
    email: EmailStr
    username: str
    password: str
    photo: Optional[str]


class UserOut(BaseModel):
    username: str
    email: str
    operation_result: str


# lobby models


# game models


# board models


# log models
