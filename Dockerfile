# Python 베이스 이미지 선택
FROM python:3.10-slim

# 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 필수 패키지 설치 (Playwright가 필요로 하는 OS 라이브러리 포함)
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxkbcommon0 \
    libgtk-3-0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libxshmfence1 \
    libx11-xcb1 \
    xvfb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# 종속성 복사 및 설치
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ✅ Playwright 브라우저 설치 (가장 중요!)
RUN playwright install

# 앱 파일 복사
COPY . .

# 포트 설정 (Render가 감지하는 포트)
ENV PORT=10000

# Flask 실행 명령 (포트 명시)
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "blog:app"]
