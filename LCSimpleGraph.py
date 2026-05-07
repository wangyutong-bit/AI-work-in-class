from typing_extensions import TypedDict

# 定义状态
class State(TypedDict):
    graph_state: str

# 定义节点Nodes
def node_1(state):
    print("---Node 1---")
    return {"graph_state": state['graph_state'] +"我很"}

def node_2(state):
    print("---Node 2---")
    return {"graph_state": state['graph_state'] +"高兴!"}

def node_3(state):
    print("---Node 3---")
    return {"graph_state": state['graph_state'] +"伤心!"}

# 定义边Edges
import random
from typing import Literal

def decide_mood(state) -> Literal["node_2", "node_3"]:    
    # 使用状态决定下一个访问的节点
    user_input = state['graph_state']     
    # 使用随机函数，让节点2和节点3都有一半几率运行
    if random.random() < 0.5:
        return "node_2"
    return "node_3"

# 构建图
from langgraph.graph import StateGraph, START, END

builder = StateGraph(State)
# 添加图中节点
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

# 添加图中的边，设定运行逻辑
builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

# 编译图
graph = builder.compile()

# 生成图结构的可视化图片并保存到磁盘
image_data = graph.get_graph().draw_mermaid_png()
# 指定保存图片的文件路径
file_path = 'Agent\LCSimpleGraph.png'
# 保存到磁盘
with open(file_path, 'wb') as file:
    file.write(image_data)
print(f"图片已保存到{file_path}")

# 调用图
graph_output = graph.invoke({"graph_state" : "你好，我是周老师！"})
# 输出图的运行结果
print(graph_output)
#