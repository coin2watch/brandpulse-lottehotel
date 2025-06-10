FROM python:3.10-slim

# 필수 패키지 설치 (Playwright에 필요)
RUN apt-get update && apt-get install -y \
    curl wget unzip fonts-liberation libnss3 libatk-bridge2.0-0 libxss1 \
    libasound2 libxcomposite1 libxdamage1 libxrandr2 libgtk-3-0 libgbm-dev \
    ca-certificates && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# requirements.txt 복사 및 설치
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Playwright 브라우저 설치
RUN playwright install --with-deps chromium

COPY . .

# 포트 환경 변수 정의
ENV PORT=10000

# 앱 실행 (포트 환경변수 바인딩을 $PORT로 설정)
CMD gunicorn blog:app --bind 0.0.0.0:${PORT}
