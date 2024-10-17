from typing import List

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import EmployeeResponse, EmployeeSearchFilter

employees_router = APIRouter()


@employees_router.get("/", response_model=List[EmployeeResponse])
async def get_employees(db: Session = Depends(get_db)):
    employees = db.query(User).all()
    if not employees:
        raise HTTPException(status_code=404, detail="No employees found")

    response_data = [
        EmployeeResponse(
            id=emp.id,
            first_name=emp.first_name,
            last_name=emp.last_name,
            email=emp.email,
            role=emp.role.value,  # .value orqali string qiymatini olamiz
            department=emp.department,
            position=emp.position,
            status=emp.status.value,  # .value orqali statusni ham stringga o'tkazamiz
            employment_type=emp.employment_type.value,  # .value orqali o'tkazamiz
            is_active=emp.is_active
        ) for emp in employees
    ]

    return response_data


@employees_router.get("/employees/", response_model=List[EmployeeResponse])
async def get_employees(filters: EmployeeSearchFilter = Depends(), db: Session = Depends(get_db)):
    query = db.query(User)

    if filters.first_name:
        query = query.filter(User.first_name.ilike(f"%{filters.first_name}%"))
    if filters.last_name:
        query = query.filter(User.last_name.ilike(f"%{filters.last_name}%"))
    if filters.department:
        query = query.filter(User.department == filters.department)
    if filters.status:
        query = query.filter(User.status == filters.status)
    if filters.position:
        query = query.filter(User.position == filters.position)

    employees = query.all()

    if not employees:
        raise HTTPException(status_code=404, detail="No employees found")

    response_data = [
        EmployeeResponse(
            id=emp.id,
            first_name=emp.first_name,
            last_name=emp.last_name,
            email=emp.email,
            role=emp.role.value,  # .value orqali string qiymatini olamiz
            department=emp.department,
            position=emp.position,
            status=emp.status.value,  # .value orqali statusni ham stringga o'tkazamiz
            employment_type=emp.employment_type.value,  # .value orqali o'tkazamiz
            is_active=emp.is_active
        ) for emp in employees
    ]

    return response_data