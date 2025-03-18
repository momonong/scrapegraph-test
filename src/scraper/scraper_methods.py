from scrapegraphai.graphs import SmartScraperGraph, SmartScraperMultiGraph, OmniScraperGraph
from scrapegraphai.utils import prettify_exec_info
from src.scraper.scraper_schema import ScraperTextSchema, ScraperFAQSchema

def run_smart_scraper_graph(prompt: str, source: str, config: dict):
    """
    使用 SmartScraperGraph 執行爬取（單一 URL）。

    註解說明：
        - 可使用 prompt: "List me all the FAQ with their answers"
        - source 可依需求選擇不同的 URL：
            例如: "https://oia.ncku.edu.tw/p/404-1032-235224.php?Lang=zh-tw"
    """
    fix_prompt = "請用繁體中文回答，請將所有資訊以一段完整、簡潔、清晰的文字描述，且盡量保持資料原始的敘述。每個主要資訊點之間加入換行符號（即真正的換行，而非僅僅顯示為 \\n），不要使用 JSON 格式以及 markdown 語法。"
    if "FAQ" in prompt:
        ScraperSchema = ScraperFAQSchema
        additional_prompt =  fix_prompt + "另外，請自動從內容中找出頁面的標題，並將標題存入result['title']中。"
        is_faq = True
    else:
        ScraperSchema = ScraperTextSchema
        additional_prompt = fix_prompt
        is_faq = False

    scraper = SmartScraperGraph(
        prompt = prompt + additional_prompt,
        source=source,
        config=config,
        schema=ScraperSchema,
    )
    result = scraper.run()

    if is_faq:
        title = result.get("title", "output")
    else:
        title = prompt.split("about")[1].split("in")[0].strip()

    print("\n[SmartScraperGraph] Scraping 結果：")
    print(result)
    if hasattr(scraper, "execution_info"):
        print("\n[SmartScraperGraph] 執行狀態資訊：")
        print(prettify_exec_info(scraper.execution_info))
    else:
        print("\n[SmartScraperGraph] 無法取得執行狀態資訊。")
    return result, title

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


if __name__ == "__main__":
    from src.config import init_config
    prompt = "List me all the FAQ with their answers"
    source = "https://oia.ncku.edu.tw/p/404-1032-235224.php?Lang=zh-tw"
    config = init_config()
    run_smart_scraper_graph(prompt, source, config)

