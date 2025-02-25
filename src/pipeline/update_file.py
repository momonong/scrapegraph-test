import os
import warnings
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from dotenv import load_dotenv
from tabulate import tabulate
from src.scraper.scraper_methods import run_smart_scraper_graph
from src.config import init_config  # 假設 config.py 有你共用的設定

# 載入 .env
load_dotenv()
config = init_config()

# 過濾參數的 warning
warnings.filterwarnings(
    "ignore",
    message=r"WARNING! (azure_endpoint|model_instance|model_tokens) is not default parameter\.",
)


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

def generate_result(url: str, prompt: str, config: dict) -> str:
    """
    使用 scrapegraphai 的 SmartScraperGraph 爬取指定 URL 的資料，
    並根據 prompt 產生結果。這裡假設 run_smart_scraper_graph 的參數順序為 (prompt, source, config)
    """
    return run_smart_scraper_graph(prompt, url, config)

def update_dataframe(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """遍歷 DataFrame，如果 Result 欄位為空則利用 generate_result 更新"""
    for idx, row in df.iterrows():
        if pd.isna(row.get("Result")) or str(row.get("Result")).strip() == "":
            url = row.get("URL")
            prompt = row.get("Prompt")
            print(f"處理第 {idx+2} 行:")
            print(tabulate([["URL", url], ["Prompt", prompt]], tablefmt="plain"))
            new_result = generate_result(url, prompt, config)
            df.at[idx, "Result"] = new_result
            print(f"更新結果： {new_result}\n")
        else:
            print(f"第 {idx+2} 行已有結果，跳過。\n")
    return df

def write_back_sheet(worksheet, df: pd.DataFrame):
    """將更新後的 DataFrame 轉換成二維列表（所有欄位轉成字串），並從 A1 開始更新試算表"""
    # 將所有欄位轉換為字串，避免結構化資料導致錯誤
    df = df.fillna("").astype(str)
    data = [df.columns.tolist()] + df.values.tolist()
    worksheet.update(values=data, range_name="A1")
    print("試算表更新成功！")


# def main():
#     # 取得共用設定 (例如模型參數等)
#     config = init_config()
    
#     # 建立 gspread 客戶端，並讀取試算表
#     client, sheet_id = get_gspread_client()
#     df, worksheet = read_sheet(client, sheet_id, "Sheet1")
    
#     print("原始資料預覽：")
#     print(tabulate(df.head(), headers="keys", tablefmt="grid", showindex=False))
#     print("\n")
    
#     # 更新 DataFrame 中的 Result 欄位
#     df_updated = update_dataframe(df, config)
    
#     # 寫回試算表
#     write_back_sheet(worksheet, df_updated)

# if __name__ == "__main__":
#     main()