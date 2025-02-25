# src/main.py
import warnings
from src.scraper import scraper_methods
from src.config import init_config

# 過濾參數的 warning
warnings.filterwarnings(
    "ignore",
    message=r"WARNING! (azure_endpoint|model_instance|model_tokens) is not default parameter\.",
)

def main():
    # 初始化共用的圖形設定
    config = init_config()

    # 設定各方法的 prompt 與 source（依需求修改）
    prompt_graph = "List me all the FAQ with their answers"
    source_graph = "https://oia.ncku.edu.tw/p/404-1032-235224.php?Lang=zh-tw"
    
    prompt_multi = "List me all the FAQ with their answers"
    source_multi = [
        "https://oia.ncku.edu.tw/p/404-1032-229844.php?Lang=zh-tw",
        "https://oia.ncku.edu.tw/p/404-1032-235224.php?Lang=zh-tw"
    ]
    
    prompt_omni = "List me all the 校區 in NCKU"
    source_omni = "https://oia.ncku.edu.tw/p/404-1032-230305.php?Lang=zh-tw"

    print("=== 執行 SmartScraperGraph ===")
    scraper_methods.run_smart_scraper_graph(prompt_graph, source_graph, config)

    print("\n=== 執行 SmartScraperMultiGraph ===")
    scraper_methods.run_smart_scraper_multi_graph(prompt_multi, source_multi, config)

    print("\n=== 執行 OmniScraperGraph ===")
    scraper_methods.run_omni_scraper_graph(prompt_omni, source_omni, config)

if __name__ == "__main__":
    main()
