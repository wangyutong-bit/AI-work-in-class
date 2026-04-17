from langchain_openai import ChatOpenAI

from dotenv import load_dotenv, find_dotenv
import os
from openai import OpenAI


_ = load_dotenv(find_dotenv()) 

model = ChatOpenAI(
    api_key=os.getenv("SILICONFLOW_API_KEY"),  # 如果您没有配置环境变量，请在此处用您的API Key进行替换
    base_url="https://api.siliconflow.cn/v1",  # 填写DashScope SDK的base_url
    model="Qwen/Qwen2.5-7B-Instruct")

print(model.invoke("你好, Langchain!").content)