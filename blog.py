from playwright.sync_api import sync_playwright
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
import openai
from flask import Flask

app = Flask(__name__)

# 구글 시트 인증
def get_worksheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not creds_json:
        raise ValueError("❌ GOOGLE_SERVICE_ACCOUNT_JSON 환경변수가 없습니다.")
    with open("gcp_creds.json", "w") as f:
        f.write(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_name("gcp_creds.json", scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open("BrandPulse_LotteHotel")
    worksheet = spreadsheet.worksheet("BlogData")
    return worksheet

# ChatGPT 감정 분석
def analyze_sentiment(text):
    openai.api_key = os.environ.get("OPENAI_API_KEY")
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
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://search.naver.com/search.naver?where=view&query={keyword}", timeout=60000)
        page.wait_for_selector("a.api_txt_lines.total_tit", timeout=10000)
        elements = page.query_selector_all("a.api_txt_lines.total_tit")
        for el in elements[:5]:
            title = el.inner_text()
            link = el.get_attribute("href")
            sentiment = analyze_sentiment(title)
            results.append([
                datetime.now().strftime("%Y-%m-%d"),
                keyword,
                title,
                "-",  # 긍정/부정 키워드 추출 예정 자리
                sentiment,
                link
            ])
        browser.close()
    return results

# 실행 및 저장
def run_blog_crawler():
    worksheet = get_worksheet()
    keywords = ["롯데호텔", "신라호텔", "조선호텔", "베스트웨스턴"]
    for keyword in keywords:
        try:
            data = crawl_naver_blog(keyword)
            worksheet.append_rows(data, value_input_option="USER_ENTERED")
        except Exception as e:
            print(f"❌ {keyword} 크롤링 실패: {e}")

@app.route("/")
def index():
    try:
        run_blog_crawler()
        return "✅ BlogData updated"
    except Exception as e:
        return f"❌ Error: {e}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
