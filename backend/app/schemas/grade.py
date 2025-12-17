from pydantic import BaseModel


class GradeCreate(BaseModel):
    student_id: int
    subject: str
    score: float


class GradeResponse(BaseModel):
    id: int
    student_id: int
    subject: str
    score: float

    class Config:
        from_attributes = True
