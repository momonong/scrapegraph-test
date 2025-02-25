import os
import msal
import requests
import json
from io import BytesIO
import pandas as pd
from dotenv import load_dotenv

# 載入 .env 檔案
load_dotenv()

def get_delegated_token():
    CLIENT_ID = os.getenv("CLIENT_ID")
    TENANT = os.getenv("TENANT", "consumers")
    SCOPES = os.getenv("SCOPES").split(",")  # 例如 "Files.ReadWrite,User.Read"
    
    app = msal.PublicClientApplication(
        CLIENT_ID, authority=f"https://login.microsoftonline.com/{TENANT}"
    )
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        raise Exception("無法啟動裝置代碼流程：" + json.dumps(flow, indent=4))
    print(flow["message"])  # 請按照提示到 https://microsoft.com/devicelogin 輸入代碼
    result = app.acquire_token_by_device_flow(flow)
    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception("取得存取權杖失敗：" + json.dumps(result, indent=4))

def download_excel_from_share(share_url: str) -> BytesIO:
    # 加入 download=1 參數以強制下載
    if "download=" not in share_url:
        if "?" in share_url:
            share_url += "&download=1"
        else:
            share_url += "?download=1"
    print("Modified Share URL:", share_url)
    response = requests.get(share_url, allow_redirects=True)
    print("Content-Type:", response.headers.get("Content-Type"))
    if response.status_code == 200:
        if "spreadsheetml" in response.headers.get("Content-Type", ""):
            print("Excel 檔案下載成功！")
            return BytesIO(response.content)
        else:
            raise Exception("下載的檔案似乎不是 Excel 格式。")
    else:
        raise Exception(f"直接下載檔案失敗：{response.status_code} {response.text}")

def process_excel(df: pd.DataFrame) -> pd.DataFrame:
    def your_scraping_function(url: str, prompt: str) -> str:
        # 這裡替換成你實際的爬蟲邏輯，這裡僅示範返回一個示例結果
        return f"爬取結果：從 {url} 使用 {prompt}"
    
    for index, row in df.iterrows():
        if pd.isna(row.get("Result")) or str(row.get("Result")).strip() == "":
            url = row.get("URL")
            prompt = row.get("Prompt")
            print(f"處理第 {index+2} 行：URL = {url}, Prompt = {prompt}")
            result = your_scraping_function(url, prompt)
            df.at[index, "Result"] = result
            print(f"更新結果：{result}")
        else:
            print(f"第 {index+2} 行已有結果，跳過。")
    return df

def upload_excel_file_personal(access_token: str, local_file_path: str, remote_path: str, user_id: str):
    """
    使用適用於個人 OneDrive 的方式上傳檔案。
    remote_path 為檔案在 OneDrive 中的完整路徑，例如 "Documents/scraper_source.xlsx"
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/octet-stream"
    }
    url = f"https://graph.microsoft.com/v1.0/users/{user_id}/drive/root:/{remote_path}:/content"
    with open(local_file_path, "rb") as f:
        data = f.read()
    response = requests.put(url, headers=headers, data=data)
    if response.status_code in [200, 201]:
        print("檔案上傳成功！")
    else:
        raise Exception(f"上傳檔案失敗：{response.status_code} {response.text}")

def main_pipeline():
    # 取得委派式存取權杖
    token = get_delegated_token()
    print("存取權杖取得成功。")
    
    SHARE_URL = os.getenv("SHARE_URL")
    excel_stream = download_excel_from_share(SHARE_URL)
    
    # 讀取 Excel 檔案
    df = pd.read_excel(excel_stream, engine="openpyxl")
    print("原始資料預覽：")
    print(df.head())
    
    # 處理資料
    df_processed = process_excel(df)
    
    # 儲存更新後的檔案至本地
    output_file = "updated_file.xlsx"
    df_processed.to_excel(output_file, index=False, engine="openpyxl")
    print(f"更新後的檔案已儲存至 {output_file}")
    
    USER_ID = os.getenv("USER_ID")
    REMOTE_PATH = os.getenv("REMOTE_PATH")
    # 上傳更新後的檔案回 OneDrive
    upload_excel_file_personal(token, output_file, REMOTE_PATH, USER_ID)

if __name__ == "__main__":
    main_pipeline()
