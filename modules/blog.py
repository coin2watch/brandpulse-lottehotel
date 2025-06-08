import requests
from bs4 import BeautifulSoup
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import json
import os
from openai import OpenAI
from modules.utils import get_worksheet, is_duplicate

# 설정
BRANDS = ["롯데호텔", "신라호텔", "조선호텔", "베스트웨스턴"]
SHEET_ID = "1j9K91M2TjxYtlt4senMTRANo9rMzpK7lvewmhJ__zNQ"
SHEET_NAME = "BlogData"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 인증
creds = Credentials.from_service_account_info(
    json.loads(os.getenv("GOOGLE_SHEETS_CREDENTIALS_JSON")),
    scopes=SCOPES
)
worksheet = get_worksheet(SHEET_ID, SHEET_NAME, creds)

def analyze_blog_with_gpt(title, snippet):
    prompt = f"""다음 블로그 글의 제목과 요약을 기반으로 주요 키워드 3개와 감정(긍정 또는 부정)을 판단해줘. 감정은 단어 하나로만 말해줘.

제목: {title}
내용 요약: {snippet}

결과 형식:
- 키워드: xxx, yyy, zzz
- 감정: 긍정 or 부정
"""
    res = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content.strip()

def crawl_naver_blog(brand):
    headers = {"User-Agent": "Mozilla/5.0"}
    query = f"https://search.naver.com/search.naver?where=post&query={brand}"
    res = requests.get(query, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    items = soup.select("div.total_wrap.api_ani_send")[:3]
    today = datetime.today().strftime("%Y-%m-%d")
    print(f"[{brand}] 검색된 블로그 수: {len(items)}")

    for item in items:
        title_el = item.select_one(".total_tit")
        if not title_el:
            continue
        title = title_el.text.strip()
        link = title_el.get("href")
        desc_el = item.select_one(".total_dsc")
        snippet = desc_el.text.strip() if desc_el else ""

        if is_duplicate(worksheet, today, brand, title):
            print(f"[중복제외] {brand} - {title}")
            continue

        gpt_result = analyze_blog_with_gpt(title, snippet)

        try:
            keywords_line = [line for line in gpt_result.split("\n") if "키워드" in line][0]
            keywords = keywords_line.split(":")[1].strip()
        except:
            keywords = "추출 실패"

        row = [today, brand, title, keywords, link]
        try:
            worksheet.append_row(row, value_input_option="USER_ENTERED")
        except Exception as e:
            print(f"[시트 저장 실패] {brand} - {title} → {e}")

        # ✅ 정확한 중복 제거 (날짜 + 브랜드 + 제목)
        if is_duplicate(worksheet, today, brand, title):
            print(f"[중복제외] {brand} - {title}")
            continue

        gpt_result = analyze_blog_with_gpt(title, snippet)

        # GPT 결과 파싱
        try:
            keywords_line = [line for line in gpt_result.split("\n") if "키워드" in line][0]
            keywords = keywords_line.split(":")[1].strip()
        except:
            keywords = "추출 실패"

        row = [today, brand, title, keywords, link]

        try:
            worksheet.append_row(row, value_input_option="USER_ENTERED")
        except Exception as e:
            print(f"[시트 저장 실패] {brand} - {title} → {e}")

def run():
    for brand in BRANDS:
        print(f"[블로그 수집] {brand}")
        crawl_naver_blog(brand)
