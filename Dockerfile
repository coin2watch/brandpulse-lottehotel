FROM python:3.10-slim

# 필수 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg libglib2.0-0 libnss3 libgconf-2-4 \
    libatk-bridge2.0-0 libxss1 libasound2 libxcomposite1 libxdamage1 \
    libxrandr2 libgtk-3-0 libgbm-dev ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# requirements 설치
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# playwright 브라우저 설치
RUN apt-get update && \
    pip install playwright && \
    playwright install --with-deps chromium

# 코드 복사
COPY . .

# 포트 환경변수 설정
ENV PORT=10000

# 앱 실행 명령
CMD ["gunicorn", "blog:app", "--bind", "0.0.0.0:$PORT"]
