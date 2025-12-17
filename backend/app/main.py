from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import auth, students, attendance, grades

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="학생 관리 시스템",
    description="출결 및 성적 관리를 위한 API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(students.router)
app.include_router(attendance.router)
app.include_router(grades.router)


@app.get("/")
def root():
    return {"message": "학생 관리 시스템 API", "docs": "/docs"}
