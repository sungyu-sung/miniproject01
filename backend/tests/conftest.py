"""pytest configuration and fixtures"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client():
    """Create a test client with a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


@pytest.fixture
def admin_token(client):
    """Create admin user and return token"""
    # Register admin
    client.post(
        "/api/auth/register",
        json={"username": "admin", "password": "admin123", "role": "admin"}
    )

    # Login
    response = client.post(
        "/api/auth/login",
        data={"username": "admin", "password": "admin123"}
    )
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(admin_token):
    """Return authorization headers"""
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def sample_student(client, auth_headers):
    """Create and return a sample student"""
    response = client.post(
        "/api/students/",
        headers=auth_headers,
        json={"name": "Test Student", "student_number": "2024001", "class_name": "Class 1"}
    )
    return response.json()
