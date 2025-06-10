FROM python:3.10-slim

# 필수 시스템 패키지 설치 (Playwright 구동을 위한 의존성 포함)
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    unzip \
    fonts-liberation \
    libnss3 \
    libatk-bridge2.0-0 \
    libxss1 \
    libasound2 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgtk-3-0 \
    libgbm-dev \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# requirements.txt 복사 및 Python 패키지 설치
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ✅ Playwright 브라우저 설치 (중요: 명시적으로 chromium만 설치)
RUN playwright install chromium

# 앱 소스 코드 복사
COPY . .

# ✅ Render에서는 render.yaml의 startCommand가 실행되므로 CMD는 생략 가능
# CMD ["gunicorn", "blog:app", "--bind", "0.0.0.0:$PORT"]
