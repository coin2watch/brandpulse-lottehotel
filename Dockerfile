FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    curl wget unzip fonts-liberation libnss3 libatk-bridge2.0-0 libxss1 \
    libasound2 libxcomposite1 libxdamage1 libxrandr2 libgtk-3-0 libgbm-dev \
    ca-certificates && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 반드시 포함!
RUN playwright install chromium

COPY . .

EXPOSE 10000

CMD ["sh", "-c", "gunicorn blog:app --bind 0.0.0.0:${PORT}"]
