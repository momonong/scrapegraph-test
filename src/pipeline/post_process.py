import os

# 設定 data 資料夾的路徑（依你的專案結構修改）
data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "data"))

# 遍歷資料夾內所有檔案
for filename in os.listdir(data_folder):
    if " and related l" in filename:
        new_filename = filename.replace(" and related l", "")
        old_path = os.path.join(data_folder, filename)
        new_path = os.path.join(data_folder, new_filename)
        os.rename(old_path, new_path)
        print(f"已重新命名: {filename} -> {new_filename}")
