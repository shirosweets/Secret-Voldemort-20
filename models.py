from typing import Optional
from pydantic import BaseModel, EmailStr

# users's models


class UserIn(BaseModel):
    email: EmailStr
    username: str
    password: str
    photo: Optional[str]


class UserOut(BaseModel):
    username: str
    email: str
    operation_result: str


# lobbies's models


# games's models


# boards's models


# histories's models
