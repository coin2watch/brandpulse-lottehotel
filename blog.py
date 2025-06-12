from flask import Flask
from playwright.sync_api import sync_playwright
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import openai
import os
import json
import re
import threading

app = Flask(__name__)

def get_worksheet(log):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not creds_json:
        log.append("❌ GOOGLE_SERVICE_ACCOUNT_JSON 환경변수가 없습니다.")
        raise ValueError("GOOGLE_SERVICE_ACCOUNT_JSON 환경변수가 없습니다.")
    try:
        creds_dict = json.loads(creds_json)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        spreadsheet = client.open("BrandPulse_Lotte_Hotel")
        worksheet = spreadsheet.worksheet("BlogData")
        log.append("✅ 구글시트 인증 및 접근 성공")
        return worksheet
    except Exception as e:
        log.append(f"❌ 구글시트 인증/접근 실패: {e}")
        raise

def analyze_summary(title, link, log):
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        log.append("❌ OPENAI_API_KEY 환경변수가 없습니다.")
        raise ValueError("OPENAI_API_KEY 환경변수가 없습니다.")
    prompt = f"아래 블로그 제목과 링크를 참고해서, 마케팅/소비자 반응 관점에서 2~3문장으로 요약해줘.\n\n제목: {title}\n링크: {link}"
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        summary = response.choices[0].message.content.strip()
        log.append(f"✅ 요약 성공: '{title}' -> {summary[:30]}...")
        return summary
    except Exception as e:
        log.append(f"❌ 요약 실패: {e}")
        return "요약실패"

def parse_post_date(raw_date):
    today = datetime.now()
    if "일 전" in raw_date:
        days = int(re.search(r"(\d+)일 전", raw_date).group(1))
        post_date = today - timedelta(days=days)
    elif "시간 전" in raw_date:
        post_date = today
    elif re.match(r"\d{4}\.\d{2}\.\d{2}\.$", raw_date):
        post_date = datetime.strptime(raw_date.rstrip("."), "%Y.%m.%d")
    elif re.match(r"\d{4}\.\d{2}\.\d{2}", raw_date):
        post_date = datetime.strptime(raw_date[:10], "%Y.%m.%d")
    else:
        post_date = today
    return post_date.strftime("%Y-%m-%d")

def is_this_week(post_date):
    today = datetime.now()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    post_dt = datetime.strptime(post_date, "%Y-%m-%d")
    return start.date() <= post_dt.date() <= end.date()

def get_existing_links(worksheet, log):
    try:
        links = worksheet.col_values(6)
        log.append(f"✅ 기존 링크 {len(links)}개 불러옴")
    except Exception as e:
        links = []
        log.append(f"❌ 기존 링크 불러오기 실패: {e}")
    return set(links)

def crawl_naver_blogs(keywords, log):
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 800},
            locale='ko-KR'
        )
        for keyword in keywords:
            page = context.new_page()
            url = f"https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query={keyword}"
            log.append(f"▶️ 크롤링 시작: {keyword}")
            try:
                page.goto(url, timeout=60000)
                page.wait_for_timeout(3000)
                items = page.query_selector_all("li.bx")
                log.append(f"🔎 {keyword} 검색결과 {len(items)}건")
                count = 0
                for item in items:
                    if count >= 5:
                        break
                    title_el = item.query_selector("a.title_link")
                    date_el = item.query_selector("span.sub")
                    if not title_el or not date_el:
                        log.append("❗️ title 또는 date 요소 누락")
                        continue
                    title = title_el.inner_text()
                    link = title_el.get_attribute("href")
                    raw_date = date_el.inner_text()
                    post_date = parse_post_date(raw_date)
                    if not is_this_week(post_date):
                        log.append(f"❌ 이번주 아님: {post_date}")
                        continue
                    summary = analyze_summary(title, link, log)
                    crawl_date = datetime.now().strftime("%Y-%m-%d")
                    results.append([crawl_date, post_date, keyword, title, summary, link])
                    log.append(f"✅ 수집: {title[:20]}... ({post_date})")
                    count += 1
                page.close()
            except Exception as e:
                log.append(f"❌ 크롤링 실패 ({keyword}): {e}")
        browser.close()
    return results

def run_blog_crawler(log):
    try:
        worksheet = get_worksheet(log)
        keywords = ["롯데호텔", "신라호텔", "조선호텔"]
        existing_links = get_existing_links(worksheet, log)
        data = crawl_naver_blogs(keywords, log)
        new_data = [row for row in data if row[-1] not in existing_links]
        log.append(f"필터 후 신규 데이터: {len(new_data)}건")
        if new_data:
            try:
                worksheet.append_rows(new_data, value_input_option="USER_ENTERED")
                log.append(f"✅ {len(new_data)}건의 데이터가 구글 시트에 추가되었습니다.")
            except Exception as e:
                log.append(f"❌ 구글시트 append_rows 실패: {e}")
        else:
            log.append("❌ 저장할 신규 데이터가 없습니다.")
    except Exception as e:
        log.append(f"run_blog_crawler 예외: {e}")

@app.route("/")
def index():
    return "✅ BrandPulse Blog Crawler Running"

@app.route("/run-sync")
def run_sync():
    log = []
    run_blog_crawler(log)
    return "<br>".join(log)

@app.route("/run")
def run():
    log = []
    def task():
        run_blog_crawler(log)
    t = threading.Thread(target=task)
    t.start()
    return "<br>".join(["🔥 /run 라우트 호출됨"] + log + ["(실행 중, 새로고침하면 최신 로그가 갱신되지 않습니다)"])

@app.route("/env-debug")
def env_debug():
    val = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not val:
        return "GOOGLE_SERVICE_ACCOUNT_JSON is NOT set!", 500
    return f"Length: {len(val)}<br>Start: {val[:100]}<br>End: {val[-100:]}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
