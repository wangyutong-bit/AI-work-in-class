# 2024.11.23，langchain-ollama 0.4.0 版本BUG，需要降级到0.3.3版本:   https://github.com/langchain-ai/langchain/issues/28281
from langchain_ollama.chat_models import ChatOllama  # pip install 'ollama<0.4.0'   或者 pip install langchain_ollama
from langchain.schema import HumanMessage, AIMessage

# 修改模型配置
model = ChatOllama(
    model="qwen2.5:0.5b",
    temperature=0.7,
    base_url="http://localhost:80"  # 默认端口11434，环境变量中已修改OLLAMA_HOST=127.0.0.1:80
)

messages = [HumanMessage(content="Hello, Langchain!请用中文回复")]
print(model.invoke(messages).content)

for chunk in model.stream([("human","Hello, Langchain!介绍一下你自己")]):
    print(chunk.content,end="",flush=True)