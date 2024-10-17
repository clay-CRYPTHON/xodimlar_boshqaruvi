from sqlalchemy import Column, Integer, String, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base

import enum


Base = declarative_base()

class RoleEnum(enum.Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'
    MANAGER = 'MANAGER'

class EmploymentTypeEnum(str, enum.Enum):
    REMOTE = 'REMOTE'
    IN_OFFICE = 'IN_OFFICE'


class StatusEnum(str, enum.Enum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    ON_VACATION = 'ON_VACATION'
    ON_BUSINESS_TRIP = 'ON_BUSINESS_TRIP'


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)

    role = Column(Enum(RoleEnum), default=RoleEnum.USER)
    department = Column(String, nullable=False)
    position = Column(String, nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.ACTIVE)
    employment_type = Column(Enum(EmploymentTypeEnum), default=EmploymentTypeEnum.IN_OFFICE)

    is_active = Column(Boolean, default=True)