from enum import Enum

from pydantic import BaseModel, EmailStr
from apps.common.enum import RoleEnum

class RegisterRoleEnum(str, Enum):
    STUDENT = "STUDENT"
    INSTRUCTOR = "INSTRUCTOR"

class LoginResponse(BaseModel):
    id: int
    email: EmailStr
    role: RoleEnum
    token_type: str
    access_token: str
    refresh_token: str


class RegisterSchema(BaseModel):
    email: EmailStr
    password: str
    role: RegisterRoleEnum




class RegisterResponse(BaseModel):
    pass
