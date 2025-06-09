from flask import Flask

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
