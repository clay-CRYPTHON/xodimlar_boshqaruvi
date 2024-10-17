from pydantic import BaseModel, EmailStr
from enum import Enum

from typing_extensions import Optional


class RoleEnum(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPERVISOR = "SUPERVISOR"

class StatusEnum(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class EmploymentTypeEnum(str, Enum):
    IN_OFFICE = "IN_OFFICE"
    REMOTE = "REMOTE"

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    role: RoleEnum
    department: str
    position: str
    status: StatusEnum
    employment_type: EmploymentTypeEnum
    is_active: bool

    class Config:
        use_enum_values = True  # Enum qiymatlarini string qilib o'girish

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ResetPasswordSchema(BaseModel):
    new_password: str
    confirm_password: str


class EmailSchema(BaseModel):
    email: str


class EmployeeResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    role: RoleEnum
    department: str
    position: str
    status: StatusEnum
    employment_type: EmploymentTypeEnum
    is_active: bool

    class Config:
        orm_mode = True
        use_enum_values = True  # Enumni avtomatik stringga o'tkazadi


class EmployeeSearchFilter(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    department: Optional[str] = None
    status: Optional[StatusEnum] = None
    position: Optional[str] = None