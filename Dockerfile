FROM python:3.10-slim

# 기본 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libxkbcommon0 \
    libasound2 \
    wget \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Playwright 설치
RUN pip install --no-cache-dir playwright
RUN playwright install --with-deps

# 작업 디렉토리 설정
WORKDIR /app

# 코드 복사
COPY . /app

# 서버 실행 명령
CMD ["python", "app.py"]
