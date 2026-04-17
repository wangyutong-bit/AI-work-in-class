from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    api_key="i_am_api_key",
    base_url="http://127.0.0.1:6006/v1",
    model="Qwen2.5-7B-AIGCCLASS")

response = model.stream("你好, 介绍下简述Langchain的基本模块？")
for chunk in response:
    print(chunk.content, end="")