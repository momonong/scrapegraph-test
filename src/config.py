# src/config.py
import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI, OpenAIEmbeddings

def init_config() -> dict:
    """
    初始化環境變數與模型設定，回傳 graph_config 字典。
    """
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
        "embeddings": {
            "model_instance": embedder_model_instance
        },
    }
    return graph_config
