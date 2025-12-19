# Claude 개발 컨텍스트 문서

이 문서는 Claude와 함께 개발을 이어갈 때 참고하는 문서입니다.

---

## 프로젝트 개요

**프로젝트명:** 학생 관리 시스템 (Student Management System)
**목적:** 교육기관에서 학생 정보, 출결, 성적을 효율적으로 관리하는 웹 시스템
**참고 문서:** `c:\rokey\advanced\system.md` (시스템 설계 보고서)

---

## 현재 개발 상태 (2025-12-19 기준)

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
│   │   ├── auth.py           # JWT 인증/인가 함수
│   │   ├── models/           # DB 모델
│   │   ├── schemas/          # Pydantic 스키마
│   │   └── routers/          # API 엔드포인트
│   └── requirements.txt
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
- 비밀번호 해시 (`passlib[bcrypt]`)
- OAuth2PasswordBearer 사용
- 권한 헬퍼 함수:
  - `get_current_user`: 인증된 사용자
  - `get_current_admin`: Admin만
  - `get_current_teacher_or_admin`: Teacher 또는 Admin

#### 5. 설정값 (`config.py`)

```python
DATABASE_URL = "sqlite:///./student_management.db"
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

---

## 다음 개발 작업 (TODO)

### 우선순위 높음
1. **서버 테스트 실행**
   - `cd backend && uvicorn app.main:app --reload`
   - http://localhost:8000/docs 에서 API 테스트

2. **테스트 데이터 생성**
   - Admin 계정 생성
   - 샘플 학생 데이터 등록

3. **API 테스트 코드 작성**
   - pytest 사용
   - `backend/tests/` 디렉토리 생성

### 우선순위 중간
4. **Frontend 개발**
   - 기술 선택: React.js 또는 Vue.js
   - `frontend/` 디렉토리에 구현
   - 주요 페이지:
     - 로그인 페이지
     - 대시보드
     - 학생 관리 페이지
     - 출결 관리 페이지
     - 성적 관리 페이지

5. **추가 API 기능**
   - 출결 통계 API
   - 성적 통계 API
   - 학생 검색 API

6. **통계/시각화 기능**
   - matplotlib/seaborn 활용
   - 출결 현황 차트
   - 성적 분포 그래프

### 우선순위 낮음
7. **인프라**
   - PostgreSQL 연동
   - Docker 컨테이너화
   - 클라우드 배포 (AWS/GCP/Azure)

8. **보안 강화**
   - HTTPS 적용
   - Rate limiting
   - 입력 검증 강화

9. **로그 시스템 구축**
   - 요청/응답 로깅
   - 에러 로깅
   - 로그 파일 관리

---

## 개발 시 참고사항

### 서버 실행 방법
```bash
cd c:/rokey/miniproject01
python -m venv venv
venv\Scripts\activate
pip install -r backend/requirements.txt
cd backend
uvicorn app.main:app --reload
```

### 주요 의존성
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
pydantic==2.5.3
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
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

---

## 다음 세션에서 할 일 제안

1. 서버 실행 및 API 테스트
2. Swagger UI에서 전체 플로우 테스트 (회원가입 → 로그인 → 학생등록 → 출결/성적 입력)
3. 프론트엔드 개발 시작 또는 테스트 코드 작성

---

*마지막 업데이트: 2025-12-19*
