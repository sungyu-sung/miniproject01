"""테스트 데이터 생성 스크립트"""
import requests
from datetime import date, timedelta

BASE_URL = "http://localhost:8000"

def main():
    # 1. Admin 로그인
    print("=== Admin 로그인 ===")
    login_response = requests.post(
        f"{BASE_URL}/api/auth/login",
        data={"username": "admin", "password": "admin123"}
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"토큰 발급 완료")

    # 2. 출결 등록
    print("\n=== 출결 등록 ===")
    today = date.today()

    attendances = [
        {"student_id": 1, "date": str(today), "status": "출석"},
        {"student_id": 2, "date": str(today), "status": "지각"},
        {"student_id": 3, "date": str(today), "status": "결석"},
        {"student_id": 1, "date": str(today - timedelta(days=1)), "status": "출석"},
        {"student_id": 2, "date": str(today - timedelta(days=1)), "status": "출석"},
        {"student_id": 3, "date": str(today - timedelta(days=1)), "status": "지각"},
    ]

    for att in attendances:
        response = requests.post(
            f"{BASE_URL}/api/attendance/",
            headers=headers,
            json=att
        )
        if response.status_code == 200:
            print(f"출결 등록: 학생 {att['student_id']} - {att['date']} - {att['status']}")
        else:
            print(f"출결 등록 실패: {response.json()}")

    # 3. 성적 등록
    print("\n=== 성적 등록 ===")
    grades = [
        {"student_id": 1, "subject": "국어", "score": 95},
        {"student_id": 1, "subject": "수학", "score": 88},
        {"student_id": 1, "subject": "영어", "score": 92},
        {"student_id": 2, "subject": "국어", "score": 78},
        {"student_id": 2, "subject": "수학", "score": 95},
        {"student_id": 2, "subject": "영어", "score": 85},
        {"student_id": 3, "subject": "국어", "score": 82},
        {"student_id": 3, "subject": "수학", "score": 76},
        {"student_id": 3, "subject": "영어", "score": 90},
    ]

    for grade in grades:
        response = requests.post(
            f"{BASE_URL}/api/grades/",
            headers=headers,
            json=grade
        )
        if response.status_code == 200:
            print(f"성적 등록: 학생 {grade['student_id']} - {grade['subject']} - {grade['score']}점")
        else:
            print(f"성적 등록 실패: {response.json()}")

    # 4. 데이터 확인
    print("\n=== 학생 목록 확인 ===")
    response = requests.get(f"{BASE_URL}/api/students/", headers=headers)
    for student in response.json():
        print(f"ID: {student['id']}, 이름: {student['name']}, 학번: {student['student_number']}, 반: {student['class_name']}")

    print("\n=== 출결 목록 확인 ===")
    response = requests.get(f"{BASE_URL}/api/attendance/", headers=headers)
    for att in response.json():
        print(f"학생ID: {att['student_id']}, 날짜: {att['date']}, 상태: {att['status']}")

    print("\n=== 성적 목록 확인 ===")
    response = requests.get(f"{BASE_URL}/api/grades/", headers=headers)
    for grade in response.json():
        print(f"학생ID: {grade['student_id']}, 과목: {grade['subject']}, 점수: {grade['score']}")

    print("\n✅ 테스트 데이터 생성 완료!")

if __name__ == "__main__":
    main()
