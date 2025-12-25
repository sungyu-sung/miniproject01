from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.student import Student
from app.models.user import User
from app.schemas.student import StudentCreate, StudentUpdate, StudentResponse
from app.auth import get_current_user, get_current_teacher_or_admin

router = APIRouter(prefix="/api/students", tags=["students"])


@router.get("/", response_model=List[StudentResponse])
def get_students(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    students = db.query(Student).offset(skip).limit(limit).all()
    return students


@router.get("/search", response_model=List[StudentResponse])
def search_students(
    name: Optional[str] = Query(None, description="Student name search"),
    student_number: Optional[str] = Query(None, description="Student number search"),
    class_name: Optional[str] = Query(None, description="Class name search"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search students by name, student number, or class"""
    query = db.query(Student)

    if name:
        query = query.filter(Student.name.contains(name))
    if student_number:
        query = query.filter(Student.student_number.contains(student_number))
    if class_name:
        query = query.filter(Student.class_name == class_name)

    return query.all()


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return student


@router.post("/", response_model=StudentResponse)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher_or_admin)
):
    db_student = db.query(Student).filter(
        Student.student_number == student.student_number
    ).first()
    if db_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student number already exists"
        )

    new_student = Student(**student.model_dump())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher_or_admin)
):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    update_data = student.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_student, key, value)

    db.commit()
    db.refresh(db_student)
    return db_student


@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher_or_admin)
):
    from app.models.attendance import Attendance
    from app.models.grade import Grade
    
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # 관련 데이터 먼저 삭제
    db.query(Attendance).filter(Attendance.student_id == student_id).delete(synchronize_session=False)
    db.query(Grade).filter(Grade.student_id == student_id).delete(synchronize_session=False)
    
    # 학생 삭제
    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted successfully"}

