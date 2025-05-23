# YouTube 데이터 크롤링 및 DB 저장 프로젝트

## 기본 설정

### 1. 환경 변수 설정 (.env)
프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 다음 내용을 입력하세요:
```env
# 다운로드 경로
BASE_PATH=/Users/your_name/Downloads

# YouTube 계정 정보
YOUTUBE_ID=your_email@gmail.com
YOUTUBE_PASSWORD=your_password

# PostgreSQL DB 정보
DB_HOST=your_db_host
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
```

## 실행 방법
```bash
python main.py
```
