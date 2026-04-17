from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    api_key="no_api_key",
    base_url="http://0.0.0.0:8000/v1",
    model="qwen2Qwen2.5-7B-Instruct-AIGCCLASS-SFT")

response = model.stream("你好, 如何实现LangChain的链？")
for chunk in response:
    print(chunk.content, end="")