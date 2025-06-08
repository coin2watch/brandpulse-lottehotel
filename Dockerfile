FROM python:3.10

WORKDIR /app
COPY . .

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y wget gnupg

# Python 패키지 설치
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install playwright flask

# Playwright 브라우저 설치
RUN playwright install chromium

# Flask 웹 서버 실행
CMD ["python", "app.py"]
