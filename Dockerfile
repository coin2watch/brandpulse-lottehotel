FROM python:3.10

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# ✅ 여기 추가
RUN playwright install

CMD ["python", "blog.py"]
