"""배포 서버용 학생 30명 데이터 생성 스크립트"""
import requests
from datetime import date, timedelta
import random
import sys

# 배포 서버 URL (Render)
BASE_URL = "https://miniproject01.onrender.com"

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
    print(f"=== 배포 서버에 데이터 추가 ===")
    print(f"서버 URL: {BASE_URL}")

    # 서버 연결 테스트 (Render Cold Start 대응 - 최대 120초)
    print("\n[1] 서버 연결 테스트 (Render 슬립 모드시 최대 2분 소요)...")
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=120)
        print(f"서버 상태: {response.status_code}")
    except Exception as e:
        print(f"서버 연결 실패: {e}")
        print("Render 서버가 슬립 모드일 수 있습니다. 잠시 후 다시 시도해주세요.")
        sys.exit(1)

    # Admin 로그인
    print("\n[2] Admin 로그인...")
    login_response = requests.post(
        f"{BASE_URL}/api/auth/login",
        data={"username": "admin", "password": "admin123"},
        timeout=30
    )

    if login_response.status_code != 200:
        print(f"로그인 실패: {login_response.text}")
        print("\nadmin 계정이 없을 수 있습니다. 회원가입을 시도합니다...")

        # Admin 회원가입 시도
        register_response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json={"username": "admin", "password": "admin123", "role": "admin"},
            timeout=30
        )

        if register_response.status_code == 200:
            print("Admin 계정 생성 완료!")
            login_response = requests.post(
                f"{BASE_URL}/api/auth/login",
                data={"username": "admin", "password": "admin123"},
                timeout=30
            )
        else:
            print(f"회원가입 실패: {register_response.text}")
            sys.exit(1)

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("토큰 발급 완료!")

    # 기존 학생 확인
    print("\n[3] 기존 학생 확인...")
    existing_response = requests.get(f"{BASE_URL}/api/students/", headers=headers, timeout=30)
    existing_students = existing_response.json()
    print(f"기존 학생 수: {len(existing_students)}")
    existing_numbers = {s["student_number"] for s in existing_students}

    # 학생 30명 등록
    print("\n[4] 학생 30명 등록...")
    students = []
    student_index = 1
    registered_count = 0

    while registered_count < 30:
        student_number = generate_student_number(student_index)

        if student_number in existing_numbers:
            student_index += 1
            continue

        student_data = {
            "name": generate_student_name(),
            "student_number": student_number,
            "class_name": random.choice(CLASSES)
        }

        try:
            response = requests.post(
                f"{BASE_URL}/api/students/",
                headers=headers,
                json=student_data,
                timeout=30
            )

            if response.status_code == 200:
                created = response.json()
                students.append(created)
                print(f"  [{registered_count + 1}/30] {created['name']} ({created['student_number']}) - {created['class_name']}")
                registered_count += 1
                existing_numbers.add(student_number)
            else:
                print(f"  등록 실패: {response.json()}")
        except Exception as e:
            print(f"  요청 오류: {e}")

        student_index += 1

    student_ids = [s["id"] for s in students]

    # 출결 데이터 등록 (최근 14일, 주말 제외)
    print("\n[5] 출결 데이터 등록 (최근 14일)...")
    today = date.today()
    attendance_count = 0

    for student_id in student_ids:
        for day_offset in range(14):
            check_date = today - timedelta(days=day_offset)

            if check_date.weekday() >= 5:
                continue

            rand = random.random()
            if rand < 0.80:
                status = "출석"
            elif rand < 0.90:
                status = "지각"
            else:
                status = "결석"

            try:
                response = requests.post(
                    f"{BASE_URL}/api/attendance/",
                    headers=headers,
                    json={
                        "student_id": student_id,
                        "date": str(check_date),
                        "status": status
                    },
                    timeout=30
                )
                if response.status_code == 200:
                    attendance_count += 1
            except:
                pass

    print(f"  출결 데이터 {attendance_count}건 등록 완료")

    # 성적 데이터 등록
    print("\n[6] 성적 데이터 등록...")
    grade_count = 0

    for student_id in student_ids:
        for subject in SUBJECTS:
            score = max(0, min(100, round(random.gauss(75, 15))))

            try:
                response = requests.post(
                    f"{BASE_URL}/api/grades/",
                    headers=headers,
                    json={
                        "student_id": student_id,
                        "subject": subject,
                        "score": score
                    },
                    timeout=30
                )
                if response.status_code == 200:
                    grade_count += 1
            except:
                pass

    print(f"  성적 데이터 {grade_count}건 등록 완료")

    # 결과 요약
    print("\n" + "=" * 50)
    print("데이터 생성 완료!")
    print("=" * 50)

    all_students = requests.get(f"{BASE_URL}/api/students/", headers=headers, timeout=30).json()
    all_attendance = requests.get(f"{BASE_URL}/api/attendance/", headers=headers, timeout=30).json()
    all_grades = requests.get(f"{BASE_URL}/api/grades/", headers=headers, timeout=30).json()

    print(f"\n총 학생 수: {len(all_students)}명")
    print(f"총 출결 기록: {len(all_attendance)}건")
    print(f"총 성적 기록: {len(all_grades)}건")

    print("\n[반별 학생 수]")
    class_counts = {}
    for student in all_students:
        class_name = student["class_name"]
        class_counts[class_name] = class_counts.get(class_name, 0) + 1

    for class_name in sorted(class_counts.keys()):
        print(f"  {class_name}: {class_counts[class_name]}명")


if __name__ == "__main__":
    main()
