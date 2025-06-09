from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Flask + Gunicorn on Render is working!"

@app.route("/run-blog")
def run_blog():
    return "🚀 Blog data collection executed."
