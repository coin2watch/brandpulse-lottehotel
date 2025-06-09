from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ BrandPulse is running!"

@app.route("/run-blog")
def run_blog():
    return "📝 Blog scraping is triggered (demo)"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render가 동적으로 PORT를 지정함
    app.run(host="0.0.0.0", port=port)
