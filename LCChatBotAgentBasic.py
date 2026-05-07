# 注册，settings中创建API_KEY，https://smith.langchain.com/
# .env中添加下面这行：
# LANGSMITH_API_KEY=lsv2_pt_fae6fc7b20504ef4b414fbe01ae230c7_b412xxxxx
# pip install langsmith -i https://mirrors.aliyun.com/pypi/simple/
# pip install langgraph -i https://mirrors.aliyun.com/pypi/simple/

from langchain_openai import ChatOpenAI
import os

from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages

from dotenv import load_dotenv
load_dotenv(".env")

# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_PROJECT"] = "LCChatBotAgent"

# 定义状态
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 创建图构建器
graph_builder = StateGraph(State)

# 创建大语言模型
llm = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-plus")

# 定义chatbot节点，调用大语言模型完成聊天
def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

# 添加图中节点
graph_builder.add_node("chatbot", chatbot)

# 添加图的入口点和终结点
graph_builder.set_entry_point("chatbot")
graph_builder.set_finish_point("chatbot")
# 编译图
graph = graph_builder.compile()

# 生成图结构的可视化图片并保存到磁盘
image_data = graph.get_graph().draw_mermaid_png()
# 指定保存图片的文件路径
file_path = 'Agent\LCChatBotAgentBasic.png'  
# 保存到磁盘
with open(file_path, 'wb') as file:
    file.write(image_data)
print(f"Image saved to {file_path}")

# 运行图
while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("再见!")
        break
    for event in graph.stream({"messages": [("user", user_input)]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)


# response = llm.invoke([("user", "你好")])
# print(response.content)