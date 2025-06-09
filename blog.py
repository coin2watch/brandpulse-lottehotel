from flask import Flask
from threading import Thread
from playwright.sync_api import sync_playwright
import time

app = Flask(__name__)

def crawl_naver_blog(keyword):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://search.naver.com/search.naver?where=post&query={keyword}")
        page.wait_for_timeout(3000)
        titles = page.locator("a.api_txt_lines.total_tit").all_text_contents()
        browser.close()
        return titles

def run_crawler():
    keywords = ["롯데호텔", "신라호텔", "조선호텔", "베스트웨스턴"]
    while True:
        for kw in keywords:
            print(f"[🌀] 크롤링 시작: {kw}")
            try:
                data = crawl_naver_blog(kw)
                print(f"[✅] {kw} 결과: {data[:3]}")  # 상위 3개만 출력
            except Exception as e:
                print(f"[❌] {kw} 크롤링 오류: {e}")
        time.sleep(3600)

@app.route("/")
def index():
    return "✅ BrandPulse Blog Crawler 작동 중입니다."

if __name__ == "__main__":
    Thread(target=run_crawler, daemon=True).start()
    app.run(host="0.0.0.0", port=10000)
