# main.py
from blog import crawl_naver_blog

if __name__ == "__main__":
    keyword_list = ["롯데호텔", "신라호텔", "조선호텔", "베스트웨스턴"]
    for keyword in keyword_list:
        print(f"✅ [Blog] {keyword} 수집 중...")
        posts = crawl_naver_blog(keyword)
        for post in posts:
            print(f"• {post['title']} | {post['link']}")
