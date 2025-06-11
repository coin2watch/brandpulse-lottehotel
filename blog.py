from flask import Flask
from playwright.sync_api import sync_playwright
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
import openai
import json
import threading

# 구글 시트 인증
def get_worksheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not creds_json:
        raise ValueError("❌ GOOGLE_SERVICE_ACCOUNT_JSON 환경변수가 없습니다.")
    creds_dict = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open("BrandPulse_Lotte_Hotel")
    worksheet = spreadsheet.worksheet("BlogData")
    return worksheet

# ChatGPT 감정 분석
def analyze_sentiment(text):
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("❌ OPENAI_API_KEY 환경변수가 없습니다.")
    prompt = f"아래 블로그 제목에 대한 감정 분석 결과를 '긍정', '부정', '중립' 중 하나로만 요약해줘:\n\n제목: {text}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# 블로그 수집
def crawl_naver_blog(keyword):
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page()
        try:
            print(f"▶️ 크롤링 시작: {keyword}")
            page.goto(f"https://search.naver.com/search.naver?where=view&query={keyword}", timeout=90000)
            page.wait_for_selector("a.api_txt_lines.total_tit", timeout=10000)
            elements = page.query_selector_all("a.api_txt_lines.total_tit")
            for el in elements[:5]:
                title = el.inner_text()
                link = el.get_attribute("href")
                sentiment = analyze_sentiment(title)
                results.append([datetime.now().strftime("%Y-%m-%d"), keyword, title, "-", sentiment, link])
            print(f"✅ 크롤링 성공: {keyword}, {len(results)}건")
        except Exception as e:
            print(f"❌ 크롤링 실패 ({keyword}): {str(e)}")
        finally:
            browser.close()
    return results

# 실행 및 저장
def run_blog_crawler():
    print("run_blog_crawler started")
    worksheet = get_worksheet()
    print("worksheet loaded")
    keywords = ["롯데호텔", "신라호텔", "조선호텔", "베스트웨스턴"]
    for keyword in keywords:
        print(f"crawling {keyword}")
        data = crawl_naver_blog(keyword)
        print(f"data for {keyword}: {data}")
        if data:
            worksheet.append_rows(data, value_input_option="USER_ENTERED")
            print(f"data appended for {keyword}")
        else:
            print(f"no data to append for {keyword}")

# Flask 앱 설정
app = Flask(__name__)

@app.route("/")
def index():
    return "✅ BrandPulse Blog Crawler Running"

@app.route("/run")
def run():
    threading.Thread(target=run_blog_crawler).start()
    return "✅ BlogData update started"

# 서버 시작 시 한 번 자동 실행
def start_crawler_once():
    threading.Thread(target=run_blog_crawler, daemon=True).start()

# 함수 정의가 모두 끝난 뒤에 호출!
start_crawler_once()

# 환경변수 상태 확인용 디버그 라우트
@app.route("/env-debug")
def env_debug():
    val = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not val:
        return "GOOGLE_SERVICE_ACCOUNT_JSON is NOT set!", 500
    return f"Length: {len(val)}<br>Start: {val[:100]}<br>End: {val[-100:]}"
