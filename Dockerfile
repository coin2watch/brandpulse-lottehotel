# 기본 Python 이미지
FROM python:3.10-slim

# 작업 디렉터리 생성
WORKDIR /app

# 종속성 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# Flask 앱 실행 명령
CMD ["python", "app.py"]
