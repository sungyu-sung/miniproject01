# miniproject01 - 학생 관리 시스템

파이썬 심화반 프로젝트

Python 기반의 학생 관리 시스템으로, 출결 및 성적을 체계적으로 관리합니다.

## 기술 스택

### Backend
- Python 3.10+
- FastAPI
- SQLAlchemy (ORM)
- SQLite (개발) / PostgreSQL (운영)
- JWT 인증

### Frontend
- (추후 구현 예정)

## 주요 기능

- 사용자 관리 (Admin/Teacher/Student)
- 학생 정보 관리
- 출결 관리
- 성적 관리

## 설치 및 실행

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 의존성 설치
pip install -r backend/requirements.txt

# 서버 실행
cd backend
uvicorn app.main:app --reload
```

## API 문서

서버 실행 후 http://localhost:8000/docs 에서 Swagger UI를 통해 API 문서를 확인할 수 있습니다.
