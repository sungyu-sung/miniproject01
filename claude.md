# Claude 개발 컨텍스트 문서

이 문서는 Claude와 함께 개발을 이어갈 때 참고하는 문서입니다.

---

## 프로젝트 개요

**프로젝트명:** 학생 관리 시스템 (Student Management System)
**목적:** 교육기관에서 학생 정보, 출결, 성적을 효율적으로 관리하는 웹 시스템
**참고 문서:** `c:\rokey\advanced\system.md` (시스템 설계 보고서)

---

## 현재 개발 상태 (2025-12-25 11:00 기준)

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
├── frontend/                  # React 프론트엔드 (NEW)
│   ├── src/
│   │   ├── api/index.js      # Axios API 클라이언트
│   │   ├── context/AuthContext.jsx  # 인증 상태 관리
│   │   ├── components/Layout.jsx    # 공통 레이아웃
│   │   ├── pages/
│   │   │   ├── Login.jsx     # 로그인 페이지
│   │   │   ├── Dashboard.jsx # 대시보드
│   │   │   ├── Students.jsx  # 학생 관리
│   │   │   ├── Attendance.jsx# 출결 관리
│   │   │   └── Grades.jsx    # 성적 관리
│   │   ├── App.jsx           # 라우팅 설정
│   │   ├── main.jsx          # 엔트리포인트
│   │   └── index.css         # Tailwind CSS
│   ├── package.json
│   └── vite.config.js
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
- 학생 30명: 한국 이름 학생 데이터 (seed_30_students.py로 생성)
- 출결 약 600건 (최근 30일, 주말 제외)
- 성적 180건 (국어, 수학, 영어, 과학, 사회, 역사 - 학생당 6과목)

#### 7. 프론트엔드 필터 기능

- **학생 관리 (Students.jsx)**
  - 이름, 학번, 반으로 실시간 필터링
  - 초기화 버튼 및 필터 결과 카운트 표시

- **출결 관리 (Attendance.jsx)**
  - 학생 이름, 날짜, 상태(출석/지각/결석)로 필터링
  - 초기화 버튼 및 필터 결과 카운트 표시

- **성적 관리 (Grades.jsx)**
  - 학생 이름, 과목으로 필터링
  - 초기화 버튼 및 필터 결과 카운트 표시

---

## 다음 개발 작업 (TODO)

### 완료됨
1. ~~**Frontend 개발**~~ ✅
   - React.js + Vite + Tailwind CSS v4
   - 모든 페이지 구현 완료 (로그인, 대시보드, 학생/출결/성적 관리)

2. ~~**필터 기능 구현**~~ ✅
   - 학생/출결/성적 관리 페이지 필터 추가
   - 실시간 클라이언트 사이드 필터링
   - 초기화 버튼 및 결과 카운트 표시

3. ~~**데이터베이스 초기화**~~ ✅
   - 30명 한국 이름 학생 데이터 생성
   - 출결 API limit 수정 (100 → 10000)

### 우선순위 높음
2. **추가 API 기능**
   - [ ] 출결 통계 API (출석률 계산, 기간별 통계)
   - [ ] 성적 통계 API (평균, 석차, 과목별 분석)
   - [ ] 학생 검색 API (이름, 학번으로 검색)

### 우선순위 중간
3. **대시보드 차트 시각화**
   - [ ] Chart.js 또는 Recharts 라이브러리 연동
   - [ ] 출결 현황 파이차트 (출석/지각/결석 비율)
   - [ ] 성적 분포 막대그래프
   - [ ] 월별 출결 추이 라인차트

4. **학생별 상세 리포트**
   - [ ] 학생 상세 페이지 구현
   - [ ] 개인별 출결 이력
   - [ ] 개인별 성적 추이 그래프

### 우선순위 낮음
5. **인프라**
   - [ ] PostgreSQL 연동
   - [ ] Docker 컨테이너화
   - [ ] 클라우드 배포 (Vercel + Railway)

6. **보안 강화**
   - [ ] HTTPS 적용
   - [ ] Rate limiting
   - [ ] 입력 검증 강화

7. **로그 시스템 구축**
   - [ ] 요청/응답 로깅
   - [ ] 에러 로깅
   - [ ] 로그 파일 관리

---

## 개발 시 참고사항

### 백엔드 서버 실행 방법
```bash
cd c:/rokey/miniproject01
source venv/Scripts/activate  # 이미 가상환경 생성됨
cd backend
uvicorn app.main:app --reload
# http://localhost:8000 에서 실행
```

### 프론트엔드 실행 방법
```bash
cd c:/rokey/miniproject01/frontend
npm run dev
# http://localhost:5173 에서 실행
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

**오후 13:30 ~ 13:45**
- React + Vite + Tailwind CSS v4 프론트엔드 구축
- 로그인 페이지 구현 (JWT 인증 연동)
- 대시보드 페이지 구현 (통계 카드, 최근 학생 목록)
- 학생 관리 페이지 구현 (CRUD 기능)
- 출결 관리 페이지 구현 (출결 등록/삭제)
- 성적 관리 페이지 구현 (성적 등록/수정/삭제)
- 프론트엔드 빌드 테스트 완료

### 2025-12-25 (Day 3)

**오전 10:00 ~ 11:00**
- 데이터베이스 초기화 및 30명 한국 이름 학생 데이터 생성
- seed_30_students.py 스크립트로 출결(약 600건), 성적(180건) 데이터 자동 생성
- 출결 관리 API limit 수정 (100 → 10000)로 전체 데이터 조회 가능하도록 개선
- 학생 삭제 시 관련 출결/성적 데이터 CASCADE 삭제 구현

**오전 10:00 ~ 11:00**
- 학생 관리 페이지 필터 기능 구현 (이름, 학번, 반)
- 출결 관리 페이지 필터 기능 구현 (학생 이름, 날짜, 상태)
- 성적 관리 페이지 필터 기능 구현 (학생 이름, 과목)
- 모든 필터에 초기화 버튼 및 "총 X건 (전체 Y건)" 카운트 표시 추가
- 클라이언트 사이드 실시간 필터링 구현

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

**오후 13:30 ~ 13:45**
- React + Vite + Tailwind CSS v4 프론트엔드 구축
- 로그인 페이지 구현 (JWT 인증 연동)
- 대시보드 페이지 구현 (통계 카드, 최근 학생 목록)
- 학생 관리 페이지 구현 (CRUD 기능)
- 출결 관리 페이지 구현 (출결 등록/삭제)
- 성적 관리 페이지 구현 (성적 등록/수정/삭제)
- 프론트엔드 빌드 테스트 완료

### 2025-12-17 (Day 1)
- 프로젝트 초기화 및 GitHub 연동
- FastAPI 백엔드 기본 구조 구축
- 데이터베이스 모델 설계 및 구현
- JWT 인증 시스템 구현
- REST API 엔드포인트 구현

---

## 다음 세션에서 할 일 제안

1. 로컬 테스트 완료 후 Vercel/Render 배포
2. 통계 API 추가 (출결률, 평균 점수 등)
3. 차트 라이브러리 연동 (Chart.js 또는 Recharts)
4. 대시보드에 시각화 차트 추가

---

*마지막 업데이트: 2025-12-25 11:00*
