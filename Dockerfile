FROM python:3.10-slim

# 필수 패키지 설치
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

WORKDIR /app

COPY requirements.txt .

# Playwright 설치 및 브라우저 설치 먼저 수행
RUN pip install --upgrade pip && \
    pip install playwright && \
    playwright install --with-deps chromium && \
    pip install -r requirements.txt

COPY . .

ENV PORT=10000

CMD ["gunicorn", "blog:app", "--bind", "0.0.0.0:$PORT"]
