import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ BrandPulse is live!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render에서는 $PORT를 사용
    app.run(host="0.0.0.0", port=port)
