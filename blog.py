# blog.py

from flask import Flask
import threading
from modules.blog import crawl_naver_blog  # ← 정확한 모듈 경로 확인 필요

app = Flask(__name__)

@app.route("/")
def index():
    return "🌀 Blog Crawler Ready"

def run_crawler():
    keyword_list = ["롯데호텔", "신라호텔", "조선호텔", "베스트웨스턴"]
    for kw in keyword_list:
        data = crawl_naver_blog(kw)
        print(f"✅ {kw} 데이터 수집 완료")

# 서비스 시작 시 백그라운드 크롤링 실행
if __name__ == "__main__":
    threading.Thread(target=run_crawler).start()
    app.run(host="0.0.0.0", port=10000)
