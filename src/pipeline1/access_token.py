import os 
import msal
import time
from dotenv import load_dotenv

load_dotenv()

# 設定你的參數
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SCOPES = ["https://graph.microsoft.com/.default"]

def get_access_token():
    app = msal.ConfidentialClientApplication(
        client_id=CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_for_client(scopes=SCOPES)
    if "access_token" in result:
        return result
    else:
        raise Exception("取得 token 失敗：" + str(result))

if __name__ == "__main__":
    token_result = get_access_token()
    access_token = token_result["access_token"]
    expires_in = token_result.get("expires_in")  # token 有效秒數
    print("Access Token:")
    print(access_token)
    print("\nToken 有效時間 (秒):", expires_in)
    
    # 你也可以算出 token 到期的絕對時間（目前時間 + expires_in）
    expiry_timestamp = time.time() + expires_in
    print("Token 到期時間戳：", expiry_timestamp)
