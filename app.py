from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ BrandPulse Web Service is running."

# blog 모듈 import 시도
try:
    from modules import blog

    @app.route("/run-blog", methods=["GET"])
    def run_blog():
        blog.run()
        return "✅ Blog crawling done!", 200

except Exception as e:
    @app.route("/run-blog", methods=["GET"])
    def run_blog_error():
        return f"❌ Error loading blog: {str(e)}", 500

# 반드시 Render의 포트를 사용하도록 설정
if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))  # 기본값 설정해도 무방
    app.run(host="0.0.0.0", port=port)
