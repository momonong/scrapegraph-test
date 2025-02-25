import requests

def get_drive_item_info(access_token, file_path):
    """
    透過檔案路徑查詢 OneDrive 上的檔案資訊。

    :param access_token: 存取權杖
    :param file_path: 檔案在 OneDrive 中的路徑，例如 "YourExcel.xlsx"（若檔案位於根目錄），
                    或 "Folder/SubFolder/YourExcel.xlsx"
    :return: 檔案資訊的 JSON 資料，包含 itemId 以及 parentReference 中可能的 driveId。
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    # 注意：使用冒號結尾表示你要取得檔案資訊而非檔案內容
    url = f"https://graph.microsoft.com/v1.0/me/drive/root:/{file_path}:"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} {response.text}")

if __name__ == "__main__":
    # 假設你已經有 access_token
    # 輸入檔案路徑，例如檔案在根目錄中
    file_path = "scraper_source.xlsx"  
    # 若檔案在資料夾中，請使用類似 "FolderName/YourExcel.xlsx" 的格式

    # item_info = get_drive_item_info(access_token, file_path)
    print("檔案資訊：")
    # print(item_info)
    # 從輸出中，你可以找到檔案的 "id" 這就是 itemId
    # 如果需要 driveId，一般情況下，你可以透過 item_info["parentReference"]["driveId"] 取得（若存在）
