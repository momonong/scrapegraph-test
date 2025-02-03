import os
from dotenv import load_dotenv
from scrapegraphai.graphs import (
    SmartScraperGraph,
    SmartScraperMultiGraph,
    OmniScraperGraph,
)
from scrapegraphai.utils import prettify_exec_info
from langchain_openai import AzureChatOpenAI, OpenAIEmbeddings
import warnings

# 過濾參數的 warning
warnings.filterwarnings(
    "ignore",
    message=r"WARNING! (azure_endpoint|model_instance|model_tokens) is not default parameter\.",
)

load_dotenv()

# 初始化 AzureChatOpenAI 作為 LLM 模型
llm_model_instance = AzureChatOpenAI(
    api_version="2024-02-15-preview",
    top_p=1,
    presence_penalty=2,
    azure_deployment="gpt-4o",
    azure_endpoint=os.getenv("AZURE_ENDPOINT_LLM"),
    temperature=0,
    max_tokens=3500,
    api_key=os.getenv("OPENAI_API_KEY"),
)

# 初始化 OpenAIEmbeddings 作為嵌入模型
embedder_model_instance = OpenAIEmbeddings(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_version="2023-05-15",
    deployment="text-embedding-3-large",  # 直接以參數傳入
    azure_endpoint=os.getenv("AZURE_ENDPOINT_EMBEDDINGS"),
)

# 假設 model_tokens 數量為 100K
model_tokens_count = 100000
graph_config = {
    "llm": {
        "model_instance": llm_model_instance,
        "model_tokens": model_tokens_count,
    },
    "embeddings": {"model_instance": embedder_model_instance},
}

# ************************************************
# Create the SmartScraperGraph instance and run it
# ************************************************
# smart_scraper_graph = SmartScraperGraph(
#     # FAQ prompt
#     prompt="List me all the FAQ with their answers",
#     # other prompt
#     # prompt="List me the needed information about 註冊/報到 that sudents would ask in this page and write in traditional Chinese.",

#     # 國際生入學FAQ
#     # source="https://oia.ncku.edu.tw/p/404-1032-229844.php?Lang=zh-tw",
#     # 陸生入學FAQ
#     source="https://oia.ncku.edu.tw/p/404-1032-235224.php?Lang=zh-tw",
#     # 其他FAQ
#     # source="https://oia.ncku.edu.tw/p/404-1032-229841.php?Lang=zh-tw",
#     # 註冊/報到
#     # source="https://oia.ncku.edu.tw/p/404-1032-230516.php?Lang=zh-tw",

#     config=graph_config,
# )

# smart_scraper_graph = SmartScraperMultiGraph(
#     # FAQ prompt
#     prompt="List me all the FAQ with their answers",
#     # other prompt
#     # prompt="List me the needed information about 註冊/報到 that sudents would ask in this page and write in traditional Chinese.",

#     # 國際生入學FAQ + 陸生入學FAQ
#     source=[
#         "https://oia.ncku.edu.tw/p/404-1032-229844.php?Lang=zh-tw",
#         "https://oia.ncku.edu.tw/p/404-1032-235224.php?Lang=zh-tw"
#     ],

#     config=graph_config,
# )

smart_scraper_graph = OmniScraperGraph(
    # FAQ prompt
    # prompt="Explain the steps in the registration process for international students in traditional chinese.",
    # map prompt
    prompt="List me all the 校區 in NCKU",
    # other prompt
    # prompt="List me the needed information about 註冊/報到 that sudents would ask in this page and write in traditional Chinese.",

    # 院系交換生 註冊報到流程
    # source="https://oia.ncku.edu.tw/p/404-1032-230516.php?Lang=zh-tw",
    # map
    source="https://oia.ncku.edu.tw/p/404-1032-230305.php?Lang=zh-tw",

    config=graph_config,
)


print("開始執行 scraping 任務...")
result = smart_scraper_graph.run()

print("\nScraping 結果：")
print(result)

# 若 SmartScraperMultiGraph 內部儲存了執行狀態資訊，則印出
if hasattr(smart_scraper_graph, "execution_info"):
    print("\n執行狀態資訊：")
    exec_info = smart_scraper_graph.execution_info
    print(prettify_exec_info(exec_info))
else:
    print("\n無法取得執行狀態資訊。")
