# test_naver.py
import requests

def test_naver():
    url = "https://search.naver.com/search.naver?query=롯데호텔"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        print("----- Preview -----")
        print(response.text[:500])
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_naver()
