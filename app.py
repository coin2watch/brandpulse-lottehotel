import os
from flask import Flask
import traceback

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ BrandPulse Web Service is running."

try:
    from modules import blog

    @app.route("/run-blog", methods=["GET"])
    def run_blog():
        result = blog.run()
        return f"✅ Blog crawling done!\n\n{result}", 200

except Exception as e:
    print("❌ Error importing blog module:")
    traceback.print_exc()

    @app.route("/run-blog", methods=["GET"])
    def run_blog_error():
        return f"❌ Error loading blog: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render에서 포트를 읽음
    app.run(host="0.0.0.0", port=port)
