from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ BrandPulse Web Service is running."

@app.route("/run-blog")
def run_blog():
    return "✅ Blog endpoint hit!", 200
