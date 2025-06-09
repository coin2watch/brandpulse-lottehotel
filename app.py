import os
from flask import Flask
from modules import blog

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ BrandPulse Web Service is running."

@app.route("/run-blog", methods=["GET"])
def run_blog():
    blog.run()
    return "✅ Blog crawling done!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
