"""학생 30명 임의 데이터 생성 스크립트"""
import requests
from datetime import date, timedelta
import random

BASE_URL = "http://localhost:8000"

# 한국 이름 데이터
LAST_NAMES = ["김", "이", "박", "최", "정", "강", "조", "윤", "장", "임", "한", "오", "서", "신", "권", "황", "안", "송", "류", "홍"]
FIRST_NAMES = ["민준", "서준", "예준", "도윤", "시우", "하준", "주원", "지호", "지후", "준서",
               "서연", "서윤", "지우", "서현", "민서", "하윤", "수아", "지민", "지유", "채원",
               "현우", "준혁", "도현", "건우", "우진", "승현", "재민", "태민", "성민", "유진"]

# 반 이름
CLASSES = ["1-A", "1-B", "1-C", "2-A", "2-B", "2-C", "3-A", "3-B"]

# 과목
SUBJECTS = ["국어", "수학", "영어", "과학", "사회", "역사"]


def generate_student_name():
    """랜덤 한국 이름 생성"""
    return random.choice(LAST_NAMES) + random.choice(FIRST_NAMES)


def generate_student_number(index):
    """학번 생성 (2024XXXX 형식)"""
    return f"2024{str(index).zfill(4)}"


def main():
    # 1. Admin 로그인
    print("=== Admin 로그인 ===")
    login_response = requests.post(
        f"{BASE_URL}/api/auth/login",
        data={"username": "admin", "password": "admin123"}
    )

    if login_response.status_code != 200:
        print("로그인 실패! 먼저 admin 계정이 있는지 확인하세요.")
        print("서버가 실행 중인지 확인하세요: uvicorn app.main:app --reload")
        return

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("토큰 발급 완료")

    # 2. 기존 학생 확인
    print("\n=== 기존 학생 확인 ===")
    existing_response = requests.get(f"{BASE_URL}/api/students/", headers=headers)
    existing_students = existing_response.json()
    print(f"기존 학생 수: {len(existing_students)}")

    # 기존 학번 목록
    existing_numbers = {s["student_number"] for s in existing_students}

    # 3. 학생 30명 등록
    print("\n=== 학생 30명 등록 ===")
    students = []
    student_index = 1
    registered_count = 0

    while registered_count < 30:
        student_number = generate_student_number(student_index)

        # 이미 존재하는 학번이면 스킵
        if student_number in existing_numbers:
            student_index += 1
            continue

        student_data = {
            "name": generate_student_name(),
            "student_number": student_number,
            "class_name": random.choice(CLASSES)
        }

        response = requests.post(
            f"{BASE_URL}/api/students/",
            headers=headers,
            json=student_data
        )

        if response.status_code == 200:
            created = response.json()
            students.append(created)
            print(f"[{registered_count + 1}/30] 학생 등록: {created['name']} ({created['student_number']}) - {created['class_name']}")
            registered_count += 1
            existing_numbers.add(student_number)
        else:
            print(f"등록 실패: {response.json()}")

        student_index += 1

    # 새로 등록된 학생 ID 목록
    student_ids = [s["id"] for s in students]

    # 4. 출결 데이터 등록 (최근 30일)
    print("\n=== 출결 데이터 등록 (최근 30일) ===")
    today = date.today()
    attendance_count = 0

    for student_id in student_ids:
        for day_offset in range(30):
            check_date = today - timedelta(days=day_offset)

            # 주말 제외
            if check_date.weekday() >= 5:
                continue

            # 랜덤 출결 상태 (출석 80%, 지각 10%, 결석 10%)
            rand = random.random()
            if rand < 0.80:
                status = "출석"
            elif rand < 0.90:
                status = "지각"
            else:
                status = "결석"

            attendance_data = {
                "student_id": student_id,
                "date": str(check_date),
                "status": status
            }

            response = requests.post(
                f"{BASE_URL}/api/attendance/",
                headers=headers,
                json=attendance_data
            )

            if response.status_code == 200:
                attendance_count += 1

    print(f"출결 데이터 {attendance_count}건 등록 완료")

    # 5. 성적 데이터 등록
    print("\n=== 성적 데이터 등록 ===")
    grade_count = 0

    for student_id in student_ids:
        # 각 학생별로 모든 과목 성적 등록
        for subject in SUBJECTS:
            # 정규분포 기반 점수 생성 (평균 75, 표준편차 15)
            score = max(0, min(100, round(random.gauss(75, 15))))

            grade_data = {
                "student_id": student_id,
                "subject": subject,
                "score": score
            }

            response = requests.post(
                f"{BASE_URL}/api/grades/",
                headers=headers,
                json=grade_data
            )

            if response.status_code == 200:
                grade_count += 1

    print(f"성적 데이터 {grade_count}건 등록 완료")

    # 6. 결과 요약
    print("\n" + "=" * 50)
    print("데이터 생성 완료!")
    print("=" * 50)

    # 전체 학생 수 확인
    all_students = requests.get(f"{BASE_URL}/api/students/", headers=headers).json()
    all_attendance = requests.get(f"{BASE_URL}/api/attendance/", headers=headers).json()
    all_grades = requests.get(f"{BASE_URL}/api/grades/", headers=headers).json()

    print(f"총 학생 수: {len(all_students)}명")
    print(f"총 출결 기록: {len(all_attendance)}건")
    print(f"총 성적 기록: {len(all_grades)}건")

    # 반별 학생 수
    print("\n[반별 학생 수]")
    class_counts = {}
    for student in all_students:
        class_name = student["class_name"]
        class_counts[class_name] = class_counts.get(class_name, 0) + 1

    for class_name in sorted(class_counts.keys()):
        print(f"  {class_name}: {class_counts[class_name]}명")

    # 과목별 평균 점수
    print("\n[과목별 평균 점수]")
    subject_scores = {}
    for grade in all_grades:
        subject = grade["subject"]
        if subject not in subject_scores:
            subject_scores[subject] = []
        subject_scores[subject].append(grade["score"])

    for subject in SUBJECTS:
        if subject in subject_scores:
            avg = sum(subject_scores[subject]) / len(subject_scores[subject])
            print(f"  {subject}: {avg:.1f}점")


if __name__ == "__main__":
    main()
