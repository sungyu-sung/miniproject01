"""Attendance API tests"""
import pytest
from datetime import date


class TestAttendanceCreate:
    """Tests for POST /api/attendance/ endpoint"""

    def test_create_attendance_success(self, client, auth_headers, sample_student):
        """Test successful attendance creation"""
        response = client.post(
            "/api/attendance/",
            headers=auth_headers,
            json={
                "student_id": sample_student["id"],
                "date": str(date.today()),
                "status": "출석"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["student_id"] == sample_student["id"]
        assert data["status"] == "출석"

    def test_create_attendance_invalid_status(self, client, auth_headers, sample_student):
        """Test attendance creation with invalid status"""
        response = client.post(
            "/api/attendance/",
            headers=auth_headers,
            json={
                "student_id": sample_student["id"],
                "date": str(date.today()),
                "status": "invalid"
            }
        )
        assert response.status_code == 422


class TestAttendanceRead:
    """Tests for GET /api/attendance/ endpoints"""

    def test_get_attendances_empty(self, client, auth_headers):
        """Test getting attendances when empty"""
        response = client.get("/api/attendance/", headers=auth_headers)
        assert response.status_code == 200
        assert response.json() == []

    def test_get_student_attendance(self, client, auth_headers, sample_student):
        """Test getting student's attendance records"""
        # Create attendance
        client.post(
            "/api/attendance/",
            headers=auth_headers,
            json={
                "student_id": sample_student["id"],
                "date": str(date.today()),
                "status": "출석"
            }
        )

        response = client.get(
            f"/api/attendance/student/{sample_student['id']}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["student_id"] == sample_student["id"]


class TestAttendanceDelete:
    """Tests for DELETE /api/attendance/{id} endpoint"""

    def test_delete_attendance_success(self, client, auth_headers, sample_student):
        """Test successful attendance deletion"""
        # Create attendance
        create_response = client.post(
            "/api/attendance/",
            headers=auth_headers,
            json={
                "student_id": sample_student["id"],
                "date": str(date.today()),
                "status": "출석"
            }
        )
        attendance_id = create_response.json()["id"]

        # Delete
        response = client.delete(
            f"/api/attendance/{attendance_id}",
            headers=auth_headers
        )
        assert response.status_code == 200
