from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date
from typing import Optional, Union
from app.models import AttendanceStatus

class EmployeeBase(BaseModel):
    employee_id: str = Field(..., min_length=1, max_length=50)
    full_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    department: str = Field(..., min_length=1, max_length=100)

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    class Config:
        from_attributes = True

class AttendanceBase(BaseModel):
    employee_id: str
    date: date
    status: AttendanceStatus

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceUpdate(BaseModel):
    employee_id: Optional[str] = None
    date: Optional[str] = None
    status: Optional[str] = None

class AttendanceResponse(AttendanceBase):
    id: str
    
    class Config:
        from_attributes = True

class AttendanceWithEmployee(AttendanceResponse):
    employee: EmployeeResponse
    
    class Config:
        from_attributes = True
