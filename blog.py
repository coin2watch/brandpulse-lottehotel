from flask import Flask
from playwright.sync_api import sync_playwright
import threading

app = Flask(__name__)

def crawl_naver_blog(keyword):
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        search_url = f"https://search.naver.com/search.naver?where=view&query={keyword}"
        page.goto(search_url, timeout=60000)

        try:
            page.wait_for_selector("a.api_txt_lines.total_tit", timeout=5000)  # 5초로 제한
            elements = page.query_selector_all("a.api_txt_lines.total_tit")
            for element in elements[:10]:
                title = element.inner_text()
                link = element.get_attribute("href")
                results.append({'title': title, 'link': link})
        except Exception as e:
            print("❌ 크롤링 실패:", e)

        browser.close()
    return results

def run_crawler():
    print("🌀 크롤링 시작")
    keywords = ["롯데호텔", "신라호텔"]  # 원하는 키워드로 교체 가능
    for kw in keywords:
        data = crawl_naver_blog(kw)
        print(f"📋 {kw} 결과:", data)

@app.route('/')
def home():
    return "✅ Flask 서버 정상 작동 중입니다."

if __name__ == '__main__':
    threading.Thread(target=run_crawler).start()
    app.run(host='0.0.0.0', port=10000)
