from langchain_community.chat_models import ChatTongyi   # pip install dashscope
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv()) 

model = ChatTongyi(model="qwen-plus")

print(model.invoke("你好, Langchain!").content)