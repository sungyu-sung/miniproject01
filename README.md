# miniproject01 - 학생 관리 시스템

파이썬 심화반 프로젝트

Python 기반의 학생 관리 시스템으로, 출결 및 성적을 체계적으로 관리합니다.

---

## 개발 현황

### 완료된 기능
- [x] 프로젝트 초기 구조 설정
- [x] FastAPI 백엔드 기본 구조
- [x] 데이터베이스 모델 정의 (User, Student, Attendance, Grade)
- [x] JWT 기반 인증 시스템
- [x] 역할 기반 접근 제어 (RBAC: Admin/Teacher/Student)
- [x] 사용자 API (회원가입, 로그인)
- [x] 학생 관리 API (CRUD)
- [x] 출결 관리 API (등록, 조회, 삭제)
- [x] 성적 관리 API (CRUD)

### 미완료 기능 (TODO)
- [ ] Frontend 개발 (React.js 또는 Vue.js)
- [ ] PostgreSQL 운영 DB 연동
- [ ] Docker 컨테이너화
- [ ] 클라우드 배포
- [ ] API 테스트 코드 작성
- [ ] 통계/시각화 기능 (matplotlib/seaborn)
- [ ] HTTPS 적용
- [ ] 로그 시스템 구축

---

## 기술 스택

### Backend
- Python 3.10+
- FastAPI
- SQLAlchemy (ORM)
- SQLite (개발) / PostgreSQL (운영)
- JWT 인증 (python-jose)
- Pydantic (데이터 검증)

### Frontend (예정)
- React.js 또는 Vue.js

### Database
- SQLite (현재 개발용)
- PostgreSQL (운영 예정)

---

## 프로젝트 구조

```
miniproject01/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI 앱 엔트리포인트
│   │   ├── config.py         # 환경 설정
│   │   ├── database.py       # DB 연결 설정
│   │   ├── auth.py           # JWT 인증 모듈
│   │   ├── models/           # SQLAlchemy 모델
│   │   │   ├── user.py       # 사용자 모델
│   │   │   ├── student.py    # 학생 모델
│   │   │   ├── attendance.py # 출결 모델
│   │   │   └── grade.py      # 성적 모델
│   │   ├── schemas/          # Pydantic 스키마
│   │   │   ├── user.py
│   │   │   ├── student.py
│   │   │   ├── attendance.py
│   │   │   └── grade.py
│   │   └── routers/          # API 라우터
│   │       ├── auth.py       # 인증 API
│   │       ├── students.py   # 학생 API
│   │       ├── attendance.py # 출결 API
│   │       └── grades.py     # 성적 API
│   └── requirements.txt
├── frontend/                  # (추후 구현)
├── .gitignore
├── claude.md                  # 개발 이어가기용 문서
└── README.md
```

---

## 설치 및 실행

```bash
# 1. 가상환경 생성
python -m venv venv

# 2. 가상환경 활성화 (Windows)
venv\Scripts\activate

# 3. 의존성 설치
pip install -r backend/requirements.txt

# 4. 서버 실행
cd backend
uvicorn app.main:app --reload
```

---

## API 문서

서버 실행 후 아래 URL에서 API 문서를 확인할 수 있습니다:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 주요 API 엔드포인트

| Method | Endpoint | 설명 | 권한 |
|--------|----------|------|------|
| POST | /api/auth/register | 회원가입 | 모두 |
| POST | /api/auth/login | 로그인 | 모두 |
| GET | /api/students | 학생 목록 조회 | 인증 필요 |
| POST | /api/students | 학생 등록 | Teacher/Admin |
| GET | /api/attendance | 출결 목록 조회 | 인증 필요 |
| POST | /api/attendance | 출결 등록 | Teacher/Admin |
| GET | /api/grades/student/{id} | 학생 성적 조회 | 인증 필요 |
| POST | /api/grades | 성적 등록 | Teacher/Admin |

---

## 개발 일지

### 2025-12-17 (Day 1)
- 프로젝트 초기화 및 GitHub 연동
- FastAPI 백엔드 기본 구조 구축
- 데이터베이스 모델 설계 및 구현
- JWT 인증 시스템 구현
- REST API 엔드포인트 구현 (Auth, Students, Attendance, Grades)

---

## 라이선스

MIT License
