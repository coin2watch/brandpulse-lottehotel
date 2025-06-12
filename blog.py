from flask import Flask
app = Flask(__name__)

@app.route("/test-naver")
def test_naver():
    import requests
    try:
        res = requests.get(
            "https://search.naver.com/search.naver?query=롯데호텔",
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )
        return f"✅ Naver 접속 성공: {res.status_code}<br><br>{res.text[:500]}"
    except Exception as e:
        return f"❌ Naver 접속 실패: {str(e)}"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
