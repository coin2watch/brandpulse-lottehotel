import os
import json
import logging
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from openai import OpenAI
import re

# ✅ 1. 로깅 설정
logger = logging.getLogger("BrandPulse")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(console_handler)


# ✅ 2. 날짜 헬퍼
def get_today():
    return datetime.now().strftime("%Y-%m-%d")


# ✅ 3. Google Sheets 연결
def get_gsheet_client(sheet_id, sheet_name):
    creds_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not creds_json:
        logger.error("❌ GOOGLE_SERVICE_ACCOUNT_JSON 환경변수가 설정되지 않았습니다.")
        raise ValueError("GOOGLE_SERVICE_ACCOUNT_JSON 환경변수가 없습니다.")

    try:
        creds_dict = json.loads(creds_json)

        # 🔧 줄바꿈 복원 (GitHub Secrets용)
        if "private_key" in creds_dict:
            creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")

        creds = Credentials.from_service_account_info(
            creds_dict,
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        gc = gspread.authorize(creds)
        return gc.open_by_key(sheet_id).worksheet(sheet_name)

    except Exception as e:
        logger.error(f"Google Sheets 인증 실패: {e}")
        raise


# ✅ 4. 중복 체크
def is_duplicate(sheet, date, brand, title):
    rows = sheet.get_all_values()
    for row in rows[1:]:  # 헤더 제외
        if len(row) >= 3 and row[0] == date and row[1] == brand and row[2] == title:
            return True
    return False


# ✅ 5. 중복 제외 append
def append_row_if_not_exists(sheet, row, match_cols=[0, 1, 2]):
    all_rows = sheet.get_all_values()
    for r in all_rows[1:]:
        if all(r[i] == row[i] for i in match_cols if i < len(r)):
            return  # 중복인 경우
    sheet.append_row(row, value_input_option="USER_ENTERED")


# ✅ 6. 키워드 추출 (간단한 필터)
def extract_keywords_from_text(text):
    text = re.sub(r"[^\uAC00-\uD7A3a-zA-Z0-9\s]", "", text)
    words = text.split()
    keywords = [w for w in words if len(w) > 1]
    return keywords[:5]


# ✅ 7. GPT 요약
def summarize_with_gpt(text):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    try:
        res = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": f"다음 내용을 2문장 이내로 요약해줘:\n{text}"
            }],
            timeout=10
        )
        return res.choices[0].message.content.strip()
    except Exception as e:
        logger.warning(f"GPT 요약 실패: {e}")
        return "요약 실패"


# ✅ 8. 에러 무시 실행 래퍼
def safe_run(module_name, func):
    print(f"✅ [{module_name}] 실행 시작")
    try:
        func()
        print(f"✅ [{module_name}] 완료")
    except Exception as e:
        print(f"❌ [ERROR] {module_name} 실패: {e}")
