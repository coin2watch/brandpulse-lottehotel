FROM python:3.10-slim

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg fonts-liberation \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libatspi2.0-0 \
    libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 \
    libxkbcommon0 libasound2 libdrm2 libxshmfence1 libdbus-1-3 \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정 및 파일 복사
WORKDIR /app
COPY . .

# 파이썬 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install --with-deps

# 앱 실행
CMD ["python", "app.py"]

# 필수 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg fonts-liberation \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libatspi2.0-0 \
    libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 \
    libxkbcommon0 libasound2 libdrm2 libxshmfence1 libdbus-1-3 \
    && rm -rf /var/lib/apt/lists/*

# 파이썬 패키지 설치
RUN pip install --no-cache-dir playwright

# Playwright 브라우저 설치
RUN playwright install --with-deps

# 작업 디렉토리 지정 및 코드 복사
WORKDIR /app
COPY . .

# 앱 실행
CMD ["python", "app.py"]

