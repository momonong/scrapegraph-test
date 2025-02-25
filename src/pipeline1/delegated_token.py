import os
import msal
import json
import time
from dotenv import load_dotenv

load_dotenv()

def get_delegated_token():
    CLIENT_ID = os.getenv("CLIENT_ID")  # 請替換成你的真實 Client ID
    # 對於個人帳戶，tenant 應設為 "consumers"
    TENANT = "consumers"
    SCOPES = ["Files.ReadWrite", "User.Read"]

    app = msal.PublicClientApplication(
        CLIENT_ID, authority=f"https://login.microsoftonline.com/{TENANT}"
    )
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        raise Exception("無法啟動裝置代碼流程：" + json.dumps(flow, indent=4))
    print(flow["message"])  # 提示用戶到 https://microsoft.com/devicelogin 輸入代碼
    result = app.acquire_token_by_device_flow(flow)
    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception("取得存取權杖失敗：" + json.dumps(result, indent=4))

if __name__ == "__main__":
    token = get_delegated_token()
    print("取得的委派式存取權杖：")
    print(token)
