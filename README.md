# YouTube 데이터 크롤링 및 DB 저장 프로젝트

## 기본 설정

### 1. 메인 설정 (main.py)
- 기본 다운로드 경로: `/Users/isugwan/Downloads`
- YouTube 계정 정보 설정:
  ```python
  crawl_youtube("이메일", "비밀번호")
  ```

### 2. DB 설정 (upload_db.py)
- PostgreSQL 연결 정보:
  ```python
  host="localhost"
  database='studio_db'
  user="postgres"
  password='0000'
  ```

## 실행 방법
```bash
python main.py
```
