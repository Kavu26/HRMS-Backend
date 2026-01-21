from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from datetime import date

from app.database import Base, engine, get_db
from app import models, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HRMS Lite API",
    description="A lightweight Human Resource Management System API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "HRMS Lite API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/employees", response_model=schemas.EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = db.query(models.Employee).filter(
        (models.Employee.employee_id == employee.employee_id) |
        (models.Employee.email == employee.email)
    ).first()
    
    if db_employee:
        if db_employee.employee_id == employee.employee_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Employee with ID '{employee.employee_id}' already exists"
            )
        if db_employee.email == employee.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Employee with email '{employee.email}' already exists"
            )
    
    new_employee = models.Employee(
        employee_id=employee.employee_id,
        full_name=employee.full_name,
        email=employee.email,
        department=employee.department
    )
    
    try:
        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)
        return new_employee
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID or Email already exists"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating employee: {str(e)}"
        )

@app.get("/api/employees", response_model=List[schemas.EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    try:
        employees = db.query(models.Employee).all()
        return employees
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching employees: {str(e)}"
        )

@app.get("/api/employees/{employee_id}", response_model=schemas.EmployeeResponse)
def get_employee(employee_id: str, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID '{employee_id}' not found"
        )
    return employee

@app.delete("/api/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: str, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID '{employee_id}' not found"
        )
    
    try:
        db.delete(employee)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting employee: {str(e)}"
        )

@app.post("/api/attendance", response_model=schemas.AttendanceResponse, status_code=status.HTTP_201_CREATED)
def create_attendance(attendance: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.employee_id == attendance.employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID '{attendance.employee_id}' not found"
        )
    
    existing_attendance = db.query(models.Attendance).filter(
        models.Attendance.employee_id == attendance.employee_id,
        models.Attendance.date == attendance.date
    ).first()
    
    if existing_attendance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Attendance for employee '{attendance.employee_id}' on date '{attendance.date}' already exists"
        )
    
    new_attendance = models.Attendance(
        employee_id=attendance.employee_id,
        date=attendance.date,
        status=attendance.status
    )
    
    try:
        db.add(new_attendance)
        db.commit()
        db.refresh(new_attendance)
        return new_attendance
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating attendance: {str(e)}"
        )

@app.get("/api/attendance", response_model=List[schemas.AttendanceWithEmployee])
def get_all_attendance(db: Session = Depends(get_db)):
    try:
        attendance_records = db.query(models.Attendance).join(models.Employee).all()
        return attendance_records
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching attendance: {str(e)}"
        )

@app.get("/api/attendance/employee/{employee_id}", response_model=List[schemas.AttendanceResponse])
def get_employee_attendance(employee_id: str, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID '{employee_id}' not found"
        )
    
    try:
        attendance_records = db.query(models.Attendance).filter(
            models.Attendance.employee_id == employee_id
        ).order_by(models.Attendance.date.desc()).all()
        return attendance_records
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching attendance: {str(e)}"
        )

@app.get("/api/attendance/{attendance_id}", response_model=schemas.AttendanceResponse)
def get_attendance(attendance_id: str, db: Session = Depends(get_db)):
    attendance = db.query(models.Attendance).filter(models.Attendance.id == attendance_id).first()
    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Attendance record with ID '{attendance_id}' not found"
        )
    return attendance

@app.put("/api/attendance/{attendance_id}", response_model=schemas.AttendanceResponse)
def update_attendance(
    attendance_id: str, 
    attendance_update: schemas.AttendanceUpdate,
    db: Session = Depends(get_db)
):
    attendance = db.query(models.Attendance).filter(models.Attendance.id == attendance_id).first()
    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Attendance record with ID '{attendance_id}' not found"
        )
    
    # Parse date string to date object if provided
    update_date = None
    if attendance_update.date:
        try:
            update_date = date.fromisoformat(attendance_update.date)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date format. Expected YYYY-MM-DD"
            )
    
    # Parse status string to enum if provided
    update_status = None
    if attendance_update.status:
        try:
            update_status = models.AttendanceStatus(attendance_update.status)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status. Must be 'Present' or 'Absent'"
            )
    
    # Check if employee exists if employee_id is being updated
    if attendance_update.employee_id and attendance_update.employee_id != attendance.employee_id:
        employee = db.query(models.Employee).filter(models.Employee.employee_id == attendance_update.employee_id).first()
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID '{attendance_update.employee_id}' not found"
            )
        
        # Check for duplicate attendance for the new employee and date
        new_date = update_date if update_date else attendance.date
        existing_attendance = db.query(models.Attendance).filter(
            models.Attendance.employee_id == attendance_update.employee_id,
            models.Attendance.date == new_date,
            models.Attendance.id != attendance_id
        ).first()
        
        if existing_attendance:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Attendance for employee '{attendance_update.employee_id}' on date '{new_date}' already exists"
            )
    
    # Check for duplicate if date is being changed
    if update_date and update_date != attendance.date:
        check_employee_id = attendance_update.employee_id if attendance_update.employee_id else attendance.employee_id
        existing_attendance = db.query(models.Attendance).filter(
            models.Attendance.employee_id == check_employee_id,
            models.Attendance.date == update_date,
            models.Attendance.id != attendance_id
        ).first()
        
        if existing_attendance:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Attendance for employee '{check_employee_id}' on date '{update_date}' already exists"
            )
    
    # Update fields
    if attendance_update.employee_id is not None:
        attendance.employee_id = attendance_update.employee_id
    if update_date is not None:
        attendance.date = update_date
    if update_status is not None:
        attendance.status = update_status
    
    try:
        db.commit()
        db.refresh(attendance)
        return attendance
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating attendance: {str(e)}"
        )

@app.delete("/api/attendance/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attendance(attendance_id: str, db: Session = Depends(get_db)):
    attendance = db.query(models.Attendance).filter(models.Attendance.id == attendance_id).first()
    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Attendance record with ID '{attendance_id}' not found"
        )
    
    try:
        db.delete(attendance)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting attendance: {str(e)}"
        )
