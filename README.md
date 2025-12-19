# miniproject01 - 학생 관리 시스템

파이썬 심화반 프로젝트

Python 기반의 학생 관리 시스템으로, 출결 및 성적을 체계적으로 관리합니다.

---

## 개발 진행률

```
Backend API     [####################] 100%
인증 시스템      [####################] 100%
테스트 코드      [####################] 100%  (28개 테스트 통과)
Frontend        [                    ]   0%
배포/인프라      [                    ]   0%
```

**현재 단계:** Backend + 테스트 완료 → Frontend 개발 예정

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
- [x] 서버 실행 및 API 테스트 (Swagger UI)
- [x] 테스트 데이터 생성 스크립트 (seed_data.py)
- [x] pytest 기반 API 테스트 코드 (28개 테스트)

### TODO 리스트

#### 우선순위 높음 (핵심 기능)
- [ ] Frontend 개발 (React.js 또는 Vue.js)
- [ ] 추가 API 기능 (출결/성적 통계, 학생 검색)

#### 우선순위 중간 (기능 확장)
- [ ] 통계/시각화 기능 (matplotlib/seaborn)
- [ ] 대시보드 페이지

#### 우선순위 낮음 (운영 준비)
- [ ] PostgreSQL 운영 DB 연동
- [ ] Docker 컨테이너화
- [ ] 클라우드 배포 (AWS/GCP/Azure)
- [ ] HTTPS 적용 및 보안 강화
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
│   │   ├── schemas/          # Pydantic 스키마
│   │   └── routers/          # API 라우터
│   ├── tests/                 # pytest 테스트
│   │   ├── conftest.py       # 테스트 설정
│   │   ├── test_auth.py      # 인증 테스트
│   │   ├── test_students.py  # 학생 API 테스트
│   │   ├── test_attendance.py# 출결 API 테스트
│   │   └── test_grades.py    # 성적 API 테스트
│   ├── seed_data.py          # 테스트 데이터 생성
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

### 2025-12-19 (Day 2)

**오전 10:00 ~ 10:30**
- README.md 및 claude.md 문서 정리
- TODO 리스트 우선순위 정립
- 개발 진행률 시각화 추가
- GitHub 커밋/푸시

**오전 10:30 ~ 11:30**
- Python 3.14 호환성을 위한 requirements.txt 업데이트
- bcrypt 직접 사용으로 passlib 호환성 문제 해결 (auth.py 수정)
- 서버 실행 및 Swagger UI API 테스트 완료
- 테스트 데이터 생성 스크립트 작성 (seed_data.py)
- Admin 계정 + 학생 3명 + 출결 6건 + 성적 9건 등록
- pytest 기반 API 테스트 코드 작성 (28개 테스트 전체 통과)

### 2025-12-17 (Day 1)
- 프로젝트 초기화 및 GitHub 연동
- FastAPI 백엔드 기본 구조 구축
- 데이터베이스 모델 설계 및 구현
- JWT 인증 시스템 구현
- REST API 엔드포인트 구현 (Auth, Students, Attendance, Grades)

---

## 다음 작업 예정

1. **Frontend 개발** - React.js 또는 Vue.js 선택
2. **추가 API 기능** - 출결/성적 통계, 학생 검색
3. **대시보드 페이지** 구현

---

## 라이선스

MIT License
