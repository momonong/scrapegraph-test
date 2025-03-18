import os


def save_result_to_txt(result, title):
    content = result.get("text", "")
    title = title
    filename = f"{title}.txt"

    # 取得 main.py 所在的資料夾（src），再往上跳一層得到 project-root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    data_folder = os.path.join(project_root, "data")

    # 若 data 資料夾不存在就建立它
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    # 範例：將檔案存入 data 資料夾
    filepath = os.path.join(data_folder, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"結果已儲存至 {filepath}")
    return content
