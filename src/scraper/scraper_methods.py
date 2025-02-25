from scrapegraphai.graphs import SmartScraperGraph, SmartScraperMultiGraph, OmniScraperGraph
from scrapegraphai.utils import prettify_exec_info

def run_smart_scraper_graph(prompt: str, source: str, config: dict):
    """
    使用 SmartScraperGraph 執行爬取（單一 URL）。

    註解說明：
        - 可使用 prompt: "List me all the FAQ with their answers"
        - source 可依需求選擇不同的 URL：
            例如: "https://oia.ncku.edu.tw/p/404-1032-235224.php?Lang=zh-tw"
    """
    scraper = SmartScraperGraph(
        prompt=prompt,
        source=source,
        config=config,
    )
    result = scraper.run()
    print("\n[SmartScraperGraph] Scraping 結果：")
    print(result)
    if hasattr(scraper, "execution_info"):
        print("\n[SmartScraperGraph] 執行狀態資訊：")
        print(prettify_exec_info(scraper.execution_info))
    else:
        print("\n[SmartScraperGraph] 無法取得執行狀態資訊。")
    return result

def run_smart_scraper_multi_graph(prompt: str, source: list, config: dict):
    """
    使用 SmartScraperMultiGraph 執行爬取（多個 URL）。

    註解說明：
        - prompt 例如: "List me all the FAQ with their answers"
        - source：傳入一個 URL 列表，例如：
            [
                "https://oia.ncku.edu.tw/p/404-1032-229844.php?Lang=zh-tw",
                "https://oia.ncku.edu.tw/p/404-1032-235224.php?Lang=zh-tw"
            ]
    """
    scraper = SmartScraperMultiGraph(
        prompt=prompt,
        source=source,
        config=config,
    )
    result = scraper.run()
    print("\n[SmartScraperMultiGraph] Scraping 結果：")
    print(result)
    if hasattr(scraper, "execution_info"):
        print("\n[SmartScraperMultiGraph] 執行狀態資訊：")
        print(prettify_exec_info(scraper.execution_info))
    else:
        print("\n[SmartScraperMultiGraph] 無法取得執行狀態資訊。")
    return result

def run_omni_scraper_graph(prompt: str, source: str, config: dict):
    """
    使用 OmniScraperGraph 執行爬取。

    註解說明：
      - 可使用不同 prompt，例如:
          "List me all the 校區 in NCKU"
      - source 可根據需求選擇不同 URL，例如:
          "https://oia.ncku.edu.tw/p/404-1032-230305.php?Lang=zh-tw"
    """
    scraper = OmniScraperGraph(
        prompt=prompt,
        source=source,
        config=config,
    )
    result = scraper.run()
    print("\n[OmniScraperGraph] Scraping 結果：")
    print(result)
    if hasattr(scraper, "execution_info"):
        print("\n[OmniScraperGraph] 執行狀態資訊：")
        print(prettify_exec_info(scraper.execution_info))
    else:
        print("\n[OmniScraperGraph] 無法取得執行狀態資訊。")
    return result
