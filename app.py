import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ BrandPulse is live!"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))  # Render가 지정한 포트 사용
    app.run(host="0.0.0.0", port=port)
