"""Student API tests"""
import pytest


class TestStudentCreate:
    """Tests for POST /api/students/ endpoint"""

    def test_create_student_success(self, client, auth_headers):
        """Test successful student creation"""
        response = client.post(
            "/api/students/",
            headers=auth_headers,
            json={"name": "John Doe", "student_number": "2024001", "class_name": "Class 1"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "John Doe"
        assert data["student_number"] == "2024001"
        assert data["class_name"] == "Class 1"

    def test_create_student_unauthorized(self, client):
        """Test student creation without authentication"""
        response = client.post(
            "/api/students/",
            json={"name": "John Doe", "student_number": "2024001", "class_name": "Class 1"}
        )
        assert response.status_code == 401

    def test_create_student_duplicate_number(self, client, auth_headers):
        """Test student creation with duplicate student number"""
        client.post(
            "/api/students/",
            headers=auth_headers,
            json={"name": "John Doe", "student_number": "2024001", "class_name": "Class 1"}
        )
        response = client.post(
            "/api/students/",
            headers=auth_headers,
            json={"name": "Jane Doe", "student_number": "2024001", "class_name": "Class 2"}
        )
        assert response.status_code == 400


class TestStudentRead:
    """Tests for GET /api/students/ endpoints"""

    def test_get_students_empty(self, client, auth_headers):
        """Test getting students when empty"""
        response = client.get("/api/students/", headers=auth_headers)
        assert response.status_code == 200
        assert response.json() == []

    def test_get_students_list(self, client, auth_headers, sample_student):
        """Test getting students list"""
        response = client.get("/api/students/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == sample_student["name"]

    def test_get_student_by_id(self, client, auth_headers, sample_student):
        """Test getting student by ID"""
        response = client.get(
            f"/api/students/{sample_student['id']}",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["name"] == sample_student["name"]

    def test_get_student_not_found(self, client, auth_headers):
        """Test getting non-existent student"""
        response = client.get("/api/students/999", headers=auth_headers)
        assert response.status_code == 404


class TestStudentUpdate:
    """Tests for PUT /api/students/{id} endpoint"""

    def test_update_student_success(self, client, auth_headers, sample_student):
        """Test successful student update"""
        response = client.put(
            f"/api/students/{sample_student['id']}",
            headers=auth_headers,
            json={"name": "Updated Name"}
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Updated Name"

    def test_update_student_not_found(self, client, auth_headers):
        """Test updating non-existent student"""
        response = client.put(
            "/api/students/999",
            headers=auth_headers,
            json={"name": "Updated Name"}
        )
        assert response.status_code == 404


class TestStudentDelete:
    """Tests for DELETE /api/students/{id} endpoint"""

    def test_delete_student_success(self, client, auth_headers, sample_student):
        """Test successful student deletion"""
        response = client.delete(
            f"/api/students/{sample_student['id']}",
            headers=auth_headers
        )
        assert response.status_code == 200

        # Verify deletion
        get_response = client.get(
            f"/api/students/{sample_student['id']}",
            headers=auth_headers
        )
        assert get_response.status_code == 404

    def test_delete_student_not_found(self, client, auth_headers):
        """Test deleting non-existent student"""
        response = client.delete("/api/students/999", headers=auth_headers)
        assert response.status_code == 404
