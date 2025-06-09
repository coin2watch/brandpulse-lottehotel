from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ BrandPulse Web Service is running."

if __name__ == "__main__":
    port = int(os.environ["PORT"])  # 🔧 Render가 자동으로 할당한 포트 사용
    app.run(host="0.0.0.0", port=port)
