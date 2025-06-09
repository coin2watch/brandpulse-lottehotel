from flask import Flask
import threading
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ BrandPulse Blog Crawler is running"

def crawl_naver_blog(keyword):
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        search_url = f"https://search.naver.com/search.naver?where=view&query={keyword}"
        page.goto(search_url, timeout=60000)
        page.wait_for_selector("a.api_txt_lines.total_tit", timeout=10000)
        elements = page.query_selector_all("a.api_txt_lines.total_tit")
        for element in elements[:10]:
            title = element.inner_text()
            link = element.get_attribute("href")
            results.append({'title': title, 'link': link})
        browser.close()
    return results

def run_crawler():
    print("✅ [Blog] 실행 시작")
    keywords = ["롯데호텔", "신라호텔", "조선호텔", "베스트웨스턴"]
    for keyword in keywords:
        data = crawl_naver_blog(keyword)
        print(f"\n🔎 {keyword} 결과:")
        for item in data:
            print(f"📌 {item['title']} - {item['link']}")
    print("✅ [Blog] 완료")

if __name__ == "__main__":
    threading.Thread(target=run_crawler).start()
    app.run(host="0.0.0.0", port=10000)
