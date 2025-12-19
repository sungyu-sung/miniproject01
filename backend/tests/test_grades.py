"""Grade API tests"""
import pytest


class TestGradeCreate:
    """Tests for POST /api/grades/ endpoint"""

    def test_create_grade_success(self, client, auth_headers, sample_student):
        """Test successful grade creation"""
        response = client.post(
            "/api/grades/",
            headers=auth_headers,
            json={
                "student_id": sample_student["id"],
                "subject": "Math",
                "score": 95.0
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["student_id"] == sample_student["id"]
        assert data["subject"] == "Math"
        assert data["score"] == 95.0

    def test_create_grade_unauthorized(self, client, sample_student):
        """Test grade creation without authentication"""
        response = client.post(
            "/api/grades/",
            json={
                "student_id": 1,
                "subject": "Math",
                "score": 95.0
            }
        )
        assert response.status_code == 401


class TestGradeRead:
    """Tests for GET /api/grades/ endpoints"""

    def test_get_grades_empty(self, client, auth_headers):
        """Test getting grades when empty"""
        response = client.get("/api/grades/", headers=auth_headers)
        assert response.status_code == 200
        assert response.json() == []

    def test_get_student_grades(self, client, auth_headers, sample_student):
        """Test getting student's grades"""
        # Create grade
        client.post(
            "/api/grades/",
            headers=auth_headers,
            json={
                "student_id": sample_student["id"],
                "subject": "Math",
                "score": 95.0
            }
        )

        response = client.get(
            f"/api/grades/student/{sample_student['id']}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["subject"] == "Math"


class TestGradeUpdate:
    """Tests for PUT /api/grades/{id} endpoint"""

    def test_update_grade_success(self, client, auth_headers, sample_student):
        """Test successful grade update"""
        # Create grade
        create_response = client.post(
            "/api/grades/",
            headers=auth_headers,
            json={
                "student_id": sample_student["id"],
                "subject": "Math",
                "score": 95.0
            }
        )
        grade_id = create_response.json()["id"]

        # Update
        response = client.put(
            f"/api/grades/{grade_id}",
            headers=auth_headers,
            json={
                "student_id": sample_student["id"],
                "subject": "Math",
                "score": 100.0
            }
        )
        assert response.status_code == 200
        assert response.json()["score"] == 100.0


class TestGradeDelete:
    """Tests for DELETE /api/grades/{id} endpoint"""

    def test_delete_grade_success(self, client, auth_headers, sample_student):
        """Test successful grade deletion"""
        # Create grade
        create_response = client.post(
            "/api/grades/",
            headers=auth_headers,
            json={
                "student_id": sample_student["id"],
                "subject": "Math",
                "score": 95.0
            }
        )
        grade_id = create_response.json()["id"]

        # Delete
        response = client.delete(
            f"/api/grades/{grade_id}",
            headers=auth_headers
        )
        assert response.status_code == 200
