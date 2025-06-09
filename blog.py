# blog.py
from flask import Flask
from playwright.sync_api import sync_playwright
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import openai

# GPT API Key
openai.api_key = "YOUR_OPENAI_API_KEY"

app = Flask(__name__)

def crawl_naver_blog(keyword):
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        search_url = f"https://search.naver.com/search.naver?where=view&query={keyword}"
        page.goto(search_url, timeout=60000)
        page.wait_for_selector("a.api_txt_lines.total_tit", timeout=10000)
        elements = page.query_selector_all("a.api_txt_lines.total_tit")
        for element in elements[:5]:  # 상위 5개만
            title = element.inner_text()
            link = element.get_attribute("href")
            results.append({'title': title, 'link': link})
        browser.close()
    return results

def analyze_with_gpt(title):
    prompt = f"""
    아래는 브랜드 관련 블로그 글 제목이야: "{title}"
    1. 이 제목이 주는 감정(긍정/부정/중립)을 판단해줘.
    2. 주요 키워드 3개를 뽑아줘.
    형식은 다음처럼 요약해줘:
    감정 분석: [긍정/부정/중립]
    키워드: [키워드1, 키워드2, 키워드3]
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    return response.choices[0].message['content']

def save_to_google_sheets(brand, results):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("YOUR_JSON_FILENAME.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open("BrandPulseData").worksheet("BlogData")
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    for item in results:
        gpt_result = analyze_with_gpt(item['title'])

        # 감정 분석, 키워드 파싱
        sentiment_line = ""
        keyword_line = ""
        for line in gpt_result.splitlines():
            if "감정 분석" in line:
                sentiment_line = line.split(":")[-1].strip()
            elif "키워드" in line:
                keyword_line = line.split(":")[-1].strip()

        sheet.append_row([
            today,
            brand,
            item['title'],
            keyword_line,
            sentiment_line,
            item['link']
        ])

@app.route("/")
def run_crawler():
    brand = "롯데호텔"
    results = crawl_naver_blog(brand)
    save_to_google_sheets(brand, results)
    return "✅ Blog Crawling & Save Completed"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
