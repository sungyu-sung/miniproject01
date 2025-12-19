"""Authentication API tests"""
import pytest


class TestAuthRegister:
    """Tests for /api/auth/register endpoint"""

    def test_register_success(self, client):
        """Test successful user registration"""
        response = client.post(
            "/api/auth/register",
            json={"username": "testuser", "password": "testpass", "role": "student"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["role"] == "student"
        assert "id" in data

    def test_register_duplicate_username(self, client):
        """Test registration with duplicate username"""
        client.post(
            "/api/auth/register",
            json={"username": "testuser", "password": "testpass"}
        )
        response = client.post(
            "/api/auth/register",
            json={"username": "testuser", "password": "testpass2"}
        )
        assert response.status_code == 400

    def test_register_default_role(self, client):
        """Test that default role is student"""
        response = client.post(
            "/api/auth/register",
            json={"username": "testuser", "password": "testpass"}
        )
        assert response.json()["role"] == "student"


class TestAuthLogin:
    """Tests for /api/auth/login endpoint"""

    def test_login_success(self, client):
        """Test successful login"""
        # Register first
        client.post(
            "/api/auth/register",
            json={"username": "testuser", "password": "testpass"}
        )

        # Login
        response = client.post(
            "/api/auth/login",
            data={"username": "testuser", "password": "testpass"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client):
        """Test login with wrong password"""
        client.post(
            "/api/auth/register",
            json={"username": "testuser", "password": "testpass"}
        )
        response = client.post(
            "/api/auth/login",
            data={"username": "testuser", "password": "wrongpass"}
        )
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        """Test login with nonexistent user"""
        response = client.post(
            "/api/auth/login",
            data={"username": "nouser", "password": "testpass"}
        )
        assert response.status_code == 401
