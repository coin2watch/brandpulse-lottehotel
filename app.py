import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ BrandPulse Web Service is running."

try:
    print("📦 [DEBUG] blog 모듈 import 시작")
    from modules import blog
    print("✅ [DEBUG] blog 모듈 import 성공")

    @app.route("/run-blog", methods=["GET"])
    def run_blog():
        print("🚀 run_blog 라우트 실행됨")
        blog.run()
        return "✅ Blog crawling done!", 200

except Exception as e:
    import traceback
    print("❌ [DEBUG] run-blog 라우트 등록 중 에러 발생:")
    traceback.print_exc()

    @app.route("/run-blog", methods=["GET"])
    def run_blog_error():
        return f"❌ run-blog 라우트 등록 실패: {e}", 500

# DEBUG 라우트 추가
@app.route("/debug")
def debug():
    return "✅ debug 라우트 정상", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
