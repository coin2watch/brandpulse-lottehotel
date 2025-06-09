from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ BrandPulse Web Service is running."

@app.route("/run-blog", methods=["GET"])
def run_blog():
    try:
        from modules import blog
        blog.run()
        return "✅ Blog crawling done!", 200
    except Exception as e:
        return f"❌ Error: {str(e)}", 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
