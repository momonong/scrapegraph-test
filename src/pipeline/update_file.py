import os
import warnings
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from dotenv import load_dotenv
from tabulate import tabulate
from src.scraper.scraper_methods import run_smart_scraper_graph
from src.config import init_config  # 假設 config.py 有共用設定

# 過濾不必要的 warning
warnings.filterwarnings(
    "ignore",
    message=r"WARNING! (azure_endpoint|model_instance|model_tokens) is not default parameter\.",
)

# 載入環境變數
load_dotenv()
config = init_config()


def get_gspread_client():
    """根據環境變數建立 gspread 客戶端"""
    credentials_file = os.getenv("GOOGLE_CREDENTIALS_FILE")
    sheet_id = os.getenv("SHEET_ID")
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file(credentials_file, scopes=scopes)
    client = gspread.authorize(creds)
    return client, sheet_id


def read_sheet(client, sheet_id, worksheet_title="Sheet1"):
    """打開試算表並讀取資料，回傳 DataFrame 與 worksheet 物件"""
    spreadsheet = client.open_by_key(sheet_id)
    worksheet = spreadsheet.worksheet(worksheet_title)
    records = worksheet.get_all_records()  # 第一列作標題
    df = pd.DataFrame(records)
    return df, worksheet


def colnum_to_colletter(n: int) -> str:
    """將 1-indexed 的欄位數轉換成 Excel 欄位字母"""
    result = ""
    while n:
        n, remainder = divmod(n - 1, 26)
        result = chr(65 + remainder) + result
    return result


def generate_result(url: str, prompt: str, config: dict) -> str:
    """
    使用 scrapegraphai 的 SmartScraperGraph 爬取指定 URL 的資料，
    並根據 prompt 產生結果。
    假設 run_smart_scraper_graph 的參數順序為 (prompt, source, config)
    """
    return run_smart_scraper_graph(prompt, url, config)


def update_dataframe(df: pd.DataFrame, config: dict, worksheet) -> pd.DataFrame:
    """
    遍歷 DataFrame，如果 Result 欄位為空則利用 generate_result 更新，
    並立即更新試算表中對應的儲存格。
    """
    # 取得標題列，找出 "Result" 欄位的索引（1-indexed）
    header = worksheet.row_values(1)
    try:
        result_col_index = header.index("Result") + 1
    except ValueError:
        raise Exception("找不到 'Result' 欄位，請檢查試算表標題。")
    result_col_letter = colnum_to_colletter(result_col_index)
    
    for idx, row in df.iterrows():
        if pd.isna(row.get("Result")) or str(row.get("Result")).strip() == "":
            url = row.get("URL")
            prompt = row.get("Prompt")
            print(f"處理第 {idx+2} 行:")
            print(tabulate([["URL", url], ["Prompt", prompt]], tablefmt="plain"))
            new_result = generate_result(url, prompt, config)
            df.at[idx, "Result"] = new_result
            print(f"更新結果： {new_result}\n")
            # 更新試算表中該行 "Result" 欄位
            cell = f"{result_col_letter}{idx+2}"  # 第1行是標題
            worksheet.update(cell, new_result)
        else:
            print(f"第 {idx+2} 行已有結果，跳過。\n")
    return df