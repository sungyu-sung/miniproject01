# miniproject01 - 학생 관리 시스템

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/sungyu-sung/miniproject01)


파이썬 심화반 프로젝트

Python + React 기반의 학생 관리 시스템으로, 출결 및 성적을 체계적으로 관리합니다.

---

## 빠른 시작

### 필수 요구사항
- Python 3.10+
- Node.js 18+

### 설치 및 실행

```bash
# 1. 저장소 클론
git clone https://github.com/sungyu-sung/miniproject01.git
cd miniproject01

# 2. 백엔드 설정
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux
pip install -r backend/requirements.txt

# 3. 프론트엔드 설정
cd frontend
npm install
cd ..

# 4. 서버 실행 (터미널 2개 필요)
# 터미널 1: 백엔드
cd backend
uvicorn app.main:app --reload

# 터미널 2: 프론트엔드
cd frontend
npm run dev
```

### 접속
- **프론트엔드:** http://localhost:5173
- **백엔드 API:** http://localhost:8000
- **API 문서:** http://localhost:8000/docs

### 테스트 계정
| 아이디 | 비밀번호 | 권한 |
|--------|----------|------|
| admin | admin123 | 관리자 |

---

## 개발 진행률

```
Backend API     [####################] 100%
인증 시스템      [####################] 100%
테스트 코드      [####################] 100%  (28개 테스트 통과)
Frontend        [####################] 100%
배포/인프라      [                    ]   0%
```

**현재 단계:** MVP 완료 (Backend + Frontend) → 기능 고도화 예정

---

## 주요 기능

### 구현 완료
- [x] **사용자 인증** - JWT 기반 로그인/로그아웃
- [x] **학생 관리** - 등록, 수정, 삭제, 목록 조회
- [x] **출결 관리** - 출석/지각/결석 기록
- [x] **성적 관리** - 과목별 점수 등록 및 수정
- [x] **대시보드** - 통계 요약, 최근 학생 목록
- [x] **반응형 UI** - Tailwind CSS 기반 디자인
- [x] **필터 기능** - 학생/출결/성적 관리 페이지 실시간 필터링

### TODO 리스트

#### 우선순위 높음
- [x] ~~필터 기능 구현~~ (완료)
- [ ] 출결 통계 API (출석률 계산)
- [ ] 성적 통계 API (평균, 석차)

#### 우선순위 중간
- [ ] 대시보드 차트 시각화 (Chart.js / Recharts)
- [ ] 출결 현황 그래프
- [ ] 성적 분포 차트
- [ ] 학생별 상세 리포트 페이지

#### 우선순위 낮음
- [ ] PostgreSQL 운영 DB 연동
- [ ] Docker 컨테이너화
- [ ] 클라우드 배포 (Vercel + Railway)
- [ ] HTTPS 적용 및 보안 강화
- [ ] 로그 시스템 구축

---

## 기술 스택

### Backend
- **Python 3.10+** / FastAPI
- **SQLAlchemy** (ORM)
- **SQLite** (개발) / PostgreSQL (운영 예정)
- **JWT 인증** (python-jose, bcrypt)
- **Pydantic** (데이터 검증)

### Frontend
- **React 18** + Vite
- **Tailwind CSS v4**
- **React Router v6**
- **Axios** (API 통신)

### Testing
- **pytest** (28개 테스트)
- **httpx** (API 테스트 클라이언트)

---

## 프로젝트 구조

```
miniproject01/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI 앱
│   │   ├── config.py         # 환경 설정
│   │   ├── database.py       # DB 연결
│   │   ├── auth.py           # JWT 인증
│   │   ├── models/           # SQLAlchemy 모델
│   │   ├── schemas/          # Pydantic 스키마
│   │   └── routers/          # API 라우터
│   ├── tests/                # pytest 테스트 (28개)
│   ├── seed_data.py          # 테스트 데이터 생성
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/              # Axios API 클라이언트
│   │   ├── context/          # React Context (인증)
│   │   ├── components/       # 공통 컴포넌트
│   │   ├── pages/            # 페이지 컴포넌트
│   │   ├── App.jsx           # 라우팅
│   │   └── main.jsx          # 엔트리포인트
│   ├── package.json
│   └── vite.config.js
├── claude.md                 # 개발 컨텍스트 문서
└── README.md
```

---

## API 엔드포인트

| Method | Endpoint | 설명 | 권한 |
|--------|----------|------|------|
| POST | /api/auth/register | 회원가입 | 모두 |
| POST | /api/auth/login | 로그인 | 모두 |
| GET | /api/students | 학생 목록 | 인증 필요 |
| POST | /api/students | 학생 등록 | Teacher/Admin |
| PUT | /api/students/{id} | 학생 수정 | Teacher/Admin |
| DELETE | /api/students/{id} | 학생 삭제 | Admin |
| GET | /api/attendance | 출결 목록 | 인증 필요 |
| POST | /api/attendance | 출결 등록 | Teacher/Admin |
| GET | /api/grades | 성적 목록 | 인증 필요 |
| POST | /api/grades | 성적 등록 | Teacher/Admin |
| PUT | /api/grades/{id} | 성적 수정 | Teacher/Admin |

전체 API 문서: http://localhost:8000/docs

---

## 개발 일지

### 2025-12-25 (Day 3)

**오전 10:00 ~ 11:00**
- 데이터베이스 초기화 및 30명 한국 이름 학생 데이터 생성 (seed_30_students.py)
- 출결 약 600건, 성적 180건 자동 생성 (최근 30일, 주말 제외)
- 출결 관리 API limit 수정 (100 → 10000)
- 학생 삭제 시 관련 출결/성적 데이터 CASCADE 삭제 구현
- 학생/출결/성적 관리 페이지에 필터 기능 구현
  - Students.jsx: 이름, 학번, 반 필터
  - Attendance.jsx: 학생 이름, 날짜, 상태 필터
  - Grades.jsx: 학생 이름, 과목 필터
- 모든 필터에 초기화 버튼 및 결과 카운트 표시 추가
- 클라이언트 사이드 실시간 필터링 구현

### 2025-12-19 (Day 2)

**오전 10:00 ~ 11:30**
- Python 3.14 호환성을 위한 requirements.txt 업데이트
- bcrypt 직접 사용으로 passlib 호환성 문제 해결
- 서버 실행 및 Swagger UI API 테스트 완료
- 테스트 데이터 생성 스크립트 작성 (seed_data.py)
- pytest 기반 API 테스트 코드 작성 (28개 테스트 전체 통과)

**오후 13:30 ~ 14:00**
- React + Vite + Tailwind CSS v4 프론트엔드 구축
- 로그인 페이지 구현 (JWT 인증 연동)
- 대시보드 페이지 구현 (통계 카드, 최근 학생 목록)
- 학생/출결/성적 관리 페이지 구현 (CRUD 기능)
- MVP 완성

### 2025-12-17 (Day 1)
- 프로젝트 초기화 및 GitHub 연동
- FastAPI 백엔드 기본 구조 구축
- 데이터베이스 모델 설계 및 구현
- JWT 인증 시스템 구현
- REST API 엔드포인트 구현

---

## 테스트 실행

```bash
cd backend
source ../venv/Scripts/activate  # Windows: ..\venv\Scripts\activate
python -m pytest tests/ -v
```

---

## 라이선스

MIT License

---

## 개발자

- GitHub: [@sungyu-sung](https://github.com/sungyu-sung)
