import gspread
from google.oauth2.service_account import Credentials
import json
import os

# 시트 인증 및 접근
def get_worksheet(sheet_id, sheet_name):
    creds = Credentials.from_service_account_info(
        json.loads(os.getenv("GOOGLE_SHEETS_CREDENTIALS_JSON")),
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    gc = gspread.authorize(creds)
    sheet = gc.open_by_key(sheet_id)
    return sheet.worksheet(sheet_name)

# ✅ 중복 확인 함수
def is_duplicate(worksheet, check_cols, new_row_values):
    """
    worksheet: gspread worksheet 객체
    check_cols: 중복 확인할 열 인덱스 리스트 (0부터 시작)
    new_row_values: 새로 넣으려는 행 데이터 (list)

    return: True(중복), False(중복 아님)
    """
    all_rows = worksheet.get_all_values()
    for row in all_rows:
        if all(row[i] == new_row_values[i] for i in check_cols):
            return True
    return False
