FROM python:3.10-slim

# Playwright 실행에 필요한 패키지 설치
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
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# Python 패키지 설치
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install playwright && \
    playwright install --with-deps chromium && \
    pip install -r requirements.txt

# 코드 복사
COPY . .

# Render에서 자동으로 PORT 환경 변수를 주입함
ENV PORT=10000

# gunicorn 실행 (PORT 변수 사용 가능하게)
CMD ["sh", "-c", "gunicorn blog:app --bind 0.0.0.0:$PORT"]
