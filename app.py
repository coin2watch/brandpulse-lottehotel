from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ BrandPulse Web Service is running."

try:
    from modules import blog

    @app.route("/run-blog", methods=["GET"])
    def run_blog():
        blog.run()
        return "✅ Blog crawling done!", 200
except Exception as e:
    @app.route("/run-blog", methods=["GET"])
    def run_blog_error():
        return f"❌ run-blog 라우트 등록 실패: {e}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
