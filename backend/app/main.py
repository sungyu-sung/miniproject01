from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import auth, students, attendance, grades, stats

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Management System",
    description="API for attendance and grade management",
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
app.include_router(stats.router)


@app.get("/")
def root():
    return {"message": "Student Management System API", "docs": "/docs"}
