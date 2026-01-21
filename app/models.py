from sqlalchemy import Column, String, Date, ForeignKey, Enum as SQLEnum, Integer
from sqlalchemy.orm import relationship
from app.database import Base
import enum
import uuid

class AttendanceStatus(str, enum.Enum):
    PRESENT = "Present"
    ABSENT = "Absent"

class Employee(Base):
    __tablename__ = "employees"
    
    employee_id = Column(String, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    department = Column(String, nullable=False)
    
    attendance_records = relationship("Attendance", back_populates="employee", cascade="all, delete-orphan")

class Attendance(Base):
    __tablename__ = "attendance"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    employee_id = Column(String, ForeignKey("employees.employee_id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(SQLEnum(AttendanceStatus), nullable=False)
    
    employee = relationship("Employee", back_populates="attendance_records")
