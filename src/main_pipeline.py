import warnings
from tabulate import tabulate
from src.config import init_config
from src.pipeline.update_file import (
    get_gspread_client,
    read_sheet,
    update_dataframe,
    write_back_sheet,
)

# 過濾參數的 warning
warnings.filterwarnings(
    "ignore",
    message=r"WARNING! (azure_endpoint|model_instance|model_tokens) is not default parameter\.",
)


def main():
    # 取得共用設定 (例如模型參數等)
    config = init_config()

    # 建立 gspread 客戶端，並讀取試算表
    client, sheet_id = get_gspread_client()
    df, worksheet = read_sheet(client, sheet_id, "Sheet1")

    print("原始資料預覽：")
    print(tabulate(df.head(), headers="keys", tablefmt="grid", showindex=False))
    print("\n")

    # 更新 DataFrame 中的 Result 欄位
    df_updated = update_dataframe(df, config)

    # 寫回試算表
    write_back_sheet(worksheet, df_updated)


if __name__ == "__main__":
    main()
