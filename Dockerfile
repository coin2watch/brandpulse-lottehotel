FROM python:3.10-slim

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    wget gnupg curl unzip fonts-liberation libnss3 libatk-bridge2.0-0 libgtk-3-0 \
    libxss1 libasound2 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 \
    libgbm1 libpangocairo-1.0-0 libcairo2 libpangoft2-1.0-0 libjpeg-dev \
    libwoff1 libopus0 libwebp-dev libenchant-2-2 libsecret-1-dev libhyphen0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리
WORKDIR /app

# 코드 복사
COPY . .

# Python 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install --with-deps

# 포트 열기 (Render가 자동 감지)
EXPOSE 10000

# 애플리케이션 시작 명령
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "blog:app"]
