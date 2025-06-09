import os
from flask import Flask
from modules import blog  # blog.py가 modules 폴더 안에 있어야 함

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ BrandPulse Web Service is running."

@app.route("/run-blog", methods=["GET"])
def run_blog():
    try:
        blog.run()
        return "✅ Blog crawling done!", 200
    except Exception as e:
        return f"❌ Error during blog crawling: {e}", 500

if __name__ == "__main__":
    # Render가 자동으로 부여하는 포트 사용
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
