import gspread
from datetime import datetime

def get_worksheet(sheet_id, sheet_name, creds):
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(sheet_id)
    return sh.worksheet(sheet_name)

def is_duplicate(ws, date, brand, title_col=3):
    """이미 같은 날짜+브랜드+제목이 존재하는지 여부"""
    existing = ws.get_all_values()
    for row in existing[1:]:  # 헤더 제외
        if len(row) >= title_col and row[0] == date and row[1] == brand:
            return True
    return False

def safe_run(module_name, func):
    """모듈 실행 시 에러를 잡고 전체 실행이 멈추지 않도록 처리"""
    print(f"✅ [{module_name}] 실행 시작")
    try:
        func()
        print(f"✅ [{module_name}] 완료")
    except Exception as e:
        print(f"❌ [ERROR] {module_name} 실패: {e}")
