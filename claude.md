# Claude 개발 컨텍스트 문서

이 문서는 Claude와 함께 개발을 이어갈 때 참고하는 문서입니다.

---

## 프로젝트 개요

**프로젝트명:** 학생 관리 시스템 (Student Management System)
**목적:** 교육기관에서 학생 정보, 출결, 성적을 효율적으로 관리하는 웹 시스템
**참고 문서:** `c:\rokey\advanced\system.md` (시스템 설계 보고서)

---

## 현재 개발 상태 (2025-12-19 11:30 기준)

### 완료된 작업

#### 1. 프로젝트 구조
```
miniproject01/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI 앱 (CORS 설정 포함)
│   │   ├── config.py         # 환경변수 설정 (pydantic-settings)
│   │   ├── database.py       # SQLAlchemy 세션 관리
│   │   ├── auth.py           # JWT 인증/인가 함수 (bcrypt 직접 사용)
│   │   ├── models/           # DB 모델
│   │   ├── schemas/          # Pydantic 스키마
│   │   └── routers/          # API 엔드포인트
│   ├── tests/                 # pytest 테스트 (28개)
│   │   ├── conftest.py       # 테스트 설정 및 fixtures
│   │   ├── test_auth.py      # 인증 테스트 (6개)
│   │   ├── test_students.py  # 학생 API 테스트 (10개)
│   │   ├── test_attendance.py# 출결 API 테스트 (5개)
│   │   └── test_grades.py    # 성적 API 테스트 (7개)
│   ├── seed_data.py          # 테스트 데이터 생성 스크립트
│   └── requirements.txt
├── venv/                      # Python 가상환경 (Python 3.14)
├── .gitignore
├── claude.md
└── README.md
```

#### 2. 데이터베이스 모델 (SQLAlchemy)

**User** (`models/user.py`)
- id (PK), username (unique), password_hash, role (admin/teacher/student)
- UserRole Enum 정의됨

**Student** (`models/student.py`)
- id (PK), name, student_number (unique), class_name
- attendances, grades 관계 설정됨

**Attendance** (`models/attendance.py`)
- id (PK), student_id (FK), date, status (출석/지각/결석)
- AttendanceStatus Enum 정의됨

**Grade** (`models/grade.py`)
- id (PK), student_id (FK), subject, score

#### 3. API 엔드포인트

| Router | 엔드포인트 | 메서드 | 기능 |
|--------|-----------|--------|------|
| auth | /api/auth/register | POST | 회원가입 |
| auth | /api/auth/login | POST | 로그인 (JWT 발급) |
| students | /api/students | GET | 학생 목록 |
| students | /api/students/{id} | GET | 학생 상세 |
| students | /api/students | POST | 학생 등록 |
| students | /api/students/{id} | PUT | 학생 수정 |
| students | /api/students/{id} | DELETE | 학생 삭제 |
| attendance | /api/attendance | GET | 출결 목록 |
| attendance | /api/attendance/student/{id} | GET | 학생별 출결 |
| attendance | /api/attendance | POST | 출결 등록 |
| attendance | /api/attendance/{id} | DELETE | 출결 삭제 |
| grades | /api/grades | GET | 성적 목록 |
| grades | /api/grades/student/{id} | GET | 학생별 성적 |
| grades | /api/grades | POST | 성적 등록 |
| grades | /api/grades/{id} | PUT | 성적 수정 |
| grades | /api/grades/{id} | DELETE | 성적 삭제 |

#### 4. 인증/인가 시스템

- JWT 기반 인증 (`python-jose`)
- 비밀번호 해시 (`bcrypt` 직접 사용 - passlib 호환성 문제 해결)
- OAuth2PasswordBearer 사용
- 권한 헬퍼 함수:
  - `get_current_user`: 인증된 사용자
  - `get_current_admin`: Admin만
  - `get_current_teacher_or_admin`: Teacher 또는 Admin

#### 5. 테스트 코드 (pytest)

- **총 28개 테스트 전체 통과**
- 테스트 DB: SQLite in-memory
- conftest.py에 fixtures 정의 (client, admin_token, auth_headers, sample_student)

#### 6. 테스트 데이터

현재 DB에 등록된 데이터:
- Admin 계정: admin / admin123
- 학생 3명: Kim Cheolsu, Lee Younghee, Park Minsu
- 출결 6건 (2025-12-18, 2025-12-19)
- 성적 9건 (국어, 수학, 영어)

---

## 다음 개발 작업 (TODO)

### 우선순위 높음
1. **Frontend 개발**
   - 기술 선택: React.js 또는 Vue.js
   - `frontend/` 디렉토리에 구현
   - 주요 페이지:
     - 로그인 페이지
     - 대시보드
     - 학생 관리 페이지
     - 출결 관리 페이지
     - 성적 관리 페이지

2. **추가 API 기능**
   - 출결 통계 API
   - 성적 통계 API
   - 학생 검색 API

### 우선순위 중간
3. **통계/시각화 기능**
   - matplotlib/seaborn 활용
   - 출결 현황 차트
   - 성적 분포 그래프

### 우선순위 낮음
4. **인프라**
   - PostgreSQL 연동
   - Docker 컨테이너화
   - 클라우드 배포 (AWS/GCP/Azure)

5. **보안 강화**
   - HTTPS 적용
   - Rate limiting
   - 입력 검증 강화

6. **로그 시스템 구축**
   - 요청/응답 로깅
   - 에러 로깅
   - 로그 파일 관리

---

## 개발 시 참고사항

### 서버 실행 방법
```bash
cd c:/rokey/miniproject01
source venv/Scripts/activate  # 이미 가상환경 생성됨
cd backend
uvicorn app.main:app --reload
```

### 테스트 실행 방법
```bash
cd c:/rokey/miniproject01/backend
source ../venv/Scripts/activate
python -m pytest tests/ -v
```

### 주요 의존성 (Python 3.14 호환)
```
fastapi>=0.115.0
uvicorn[standard]>=0.32.0
sqlalchemy>=2.0.36
pydantic>=2.10.0
pydantic-settings>=2.6.0
python-jose[cryptography]>=3.3.0
bcrypt>=4.0.0
python-multipart>=0.0.17
requests>=2.31.0
pytest>=8.0.0
pytest-asyncio>=0.23.0
httpx>=0.27.0
```

### Git 정보
- Repository: https://github.com/sungyu-sung/miniproject01
- Branch: main

### 코드 스타일
- Python 타입 힌트 사용
- Pydantic v2 문법 (`model_dump()`, `from_attributes=True`)
- SQLAlchemy 2.0 스타일

---

## 알려진 이슈

1. **SECRET_KEY 하드코딩**
   - 운영 환경에서는 `.env` 파일로 분리 필요

2. **SQLite 사용**
   - 개발용으로만 사용, 운영시 PostgreSQL 전환 필요

3. **CORS 설정**
   - 현재 `allow_origins=["*"]`로 설정됨
   - 운영시 특정 도메인만 허용하도록 수정 필요

4. **Pydantic 경고**
   - class-based config deprecated 경고 발생
   - ConfigDict로 마이그레이션 필요

---

## 개발 히스토리

### 2025-12-19 (Day 2)

**오전 10:00 ~ 10:30**
- README.md 및 claude.md 문서 정리
- TODO 리스트 우선순위 정립
- GitHub 커밋/푸시

**오전 10:30 ~ 11:30**
- Python 3.14 호환을 위한 requirements.txt 업데이트
- passlib/bcrypt 호환성 문제 해결 (auth.py에서 bcrypt 직접 사용)
- 서버 실행 및 Swagger UI API 테스트 완료
- seed_data.py 작성 (테스트 데이터 생성 스크립트)
- pytest 테스트 코드 작성 (28개 테스트 전체 통과)

### 2025-12-17 (Day 1)
- 프로젝트 초기화 및 GitHub 연동
- FastAPI 백엔드 기본 구조 구축
- 데이터베이스 모델 설계 및 구현
- JWT 인증 시스템 구현
- REST API 엔드포인트 구현

---

## 다음 세션에서 할 일 제안

1. Frontend 개발 시작 (React.js 또는 Vue.js 선택)
2. 통계 API 추가 (출결률, 평균 점수 등)
3. 대시보드 페이지 구현

---

*마지막 업데이트: 2025-12-19 11:30*
