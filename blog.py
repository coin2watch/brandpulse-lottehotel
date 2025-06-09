blog.py

✅ NAVER 블로그에서 경쟁사 키워드 기반 상위 포스트 수집 (Playwright 기반)

from playwright.sync_api import sync_playwright

def crawl_naver_blog(keyword: str, max_count: int = 5): results = [] with sync_playwright() as p: browser = p.chromium.launch(headless=True) page = browser.new_page()

search_url = f"https://search.naver.com/search.naver?where=post&query={keyword}"
    page.goto(search_url)
    page.wait_for_timeout(3000)

    post_items = page.query_selector_all("a.api_txt_lines.total_tit")
    for post in post_items[:max_count]:
        title = post.inner_text()
        link = post.get_attribute("href")
        results.append({"keyword": keyword, "title": title, "link": link})

    browser.close()
return results

