import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ BrandPulse Web Service is running."

# DEBUG 라우트
@app.route("/debug")
def debug():
    return "✅ debug 라우트 정상", 200

# blog 라우트 밖으로 분리
@app.route("/run-blog", methods=["GET"])
def run_blog():
    try:
        from modules import blog
        print("🚀 run_blog 라우트 실행됨")
        blog.run()
        return "✅ Blog crawling done!", 200
    except Exception as e:
        import traceback
        print("❌ blog.run() 실행 중 에러:")
        traceback.print_exc()
        return f"❌ run-blog 실행 실패: {e}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
