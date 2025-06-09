import os
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
from utils import (
    logger, get_today, is_duplicate, extract_keywords_from_text,
    get_gsheet_client, summarize_with_gpt
)

# 👉 필수 환경변수: 구글 시트 ID
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

# 👉 대상 브랜드
BRANDS = ["롯데호텔", "신라호텔", "조선호텔", "베스트웨스턴"]

# ✅ 블로그 검색 함수
def search_naver_blog(brand, max_results=5):
    logger.info(f"[블로그 수집] {brand}")
    blogs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        query = f"{brand} 블로그"
        url = f"https://search.naver.com/search.naver?where=view&sm=tab_jum&query={query}"
        page.goto(url)
        page.wait_for_timeout(3000)

        items = page.query_selector_all("li.bx._svp_item")
        logger.info(f"[{brand}] 검색된 블로그 수: {len(items)}")

        for item in items[:max_results]:
            try:
                title_el = item.query_selector("a.api_txt_lines.total_tit")
                title = title_el.inner_text()
                link = title_el.get_attribute("href")
                text_snippet_el = item.query_selector("div.api_txt_lines.dsc_txt")
                snippet = text_snippet_el.inner_text() if text_snippet_el else ""
                blogs.append({"title": title, "link": link, "snippet": snippet})
            except Exception as e:
                logger.warning(f"수집 중 오류: {e}")

        browser.close()
    return blogs

# ✅ 전체 실행 함수
def run():
    try:
        logger.info("✅ [Blog] 실행 시작")
        today = get_today()

        # 시트 연결
        sheet = get_gsheet_client(SPREADSHEET_ID, "BlogData")
        insight_sheet = get_gsheet_client(SPREADSHEET_ID, "BlogInsights")

        for brand in BRANDS:
            blogs = search_naver_blog(brand)
            for blog in blogs:
                title = blog["title"]
                link = blog["link"]
                snippet = blog["snippet"]

                if is_duplicate(sheet, today, brand, title):
                    continue

                keywords = extract_keywords_from_text(title + " " + snippet)
                sentiment_keywords = [k for k in keywords if any(s in k for s in ["좋", "만족", "싫", "불만"])]
                summary = summarize_with_gpt(title + " " + snippet)

                sheet.append_row(
                    [today, brand, title, ", ".join(sentiment_keywords), link],
                    value_input_option="USER_ENTERED"
                )
                insight_sheet.append_row(
                    [today, brand, title, ", ".join(keywords), summary, link],
                    value_input_option="USER_ENTERED"
                )
                time.sleep(1)

        logger.info("✅ [Blog] 완료")
    except Exception as e:
        logger.error(f"❌ [Blog Error] {e}")
        import traceback
        traceback.print_exc()
        
