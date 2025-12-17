from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.grade import Grade
from app.models.student import Student
from app.models.user import User
from app.schemas.grade import GradeCreate, GradeResponse
from app.auth import get_current_user, get_current_teacher_or_admin

router = APIRouter(prefix="/api/grades", tags=["grades"])


@router.get("/", response_model=List[GradeResponse])
def get_grades(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    grades = db.query(Grade).offset(skip).limit(limit).all()
    return grades


@router.get("/student/{student_id}", response_model=List[GradeResponse])
def get_student_grades(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    grades = db.query(Grade).filter(Grade.student_id == student_id).all()
    return grades


@router.post("/", response_model=GradeResponse)
def create_grade(
    grade: GradeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher_or_admin)
):
    student = db.query(Student).filter(Student.id == grade.student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    new_grade = Grade(**grade.model_dump())
    db.add(new_grade)
    db.commit()
    db.refresh(new_grade)
    return new_grade


@router.put("/{grade_id}", response_model=GradeResponse)
def update_grade(
    grade_id: int,
    grade: GradeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher_or_admin)
):
    db_grade = db.query(Grade).filter(Grade.id == grade_id).first()
    if not db_grade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grade not found"
        )

    db_grade.student_id = grade.student_id
    db_grade.subject = grade.subject
    db_grade.score = grade.score

    db.commit()
    db.refresh(db_grade)
    return db_grade


@router.delete("/{grade_id}")
def delete_grade(
    grade_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher_or_admin)
):
    grade = db.query(Grade).filter(Grade.id == grade_id).first()
    if not grade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grade not found"
        )

    db.delete(grade)
    db.commit()
    return {"message": "Grade deleted successfully"}
