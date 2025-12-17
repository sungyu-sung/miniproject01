from pydantic import BaseModel
from typing import Optional


class StudentCreate(BaseModel):
    name: str
    student_number: str
    class_name: str


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    student_number: Optional[str] = None
    class_name: Optional[str] = None


class StudentResponse(BaseModel):
    id: int
    name: str
    student_number: str
    class_name: str

    class Config:
        from_attributes = True
