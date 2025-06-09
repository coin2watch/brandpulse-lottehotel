# blog.py
from playwright.sync_api import sync_playwright

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
