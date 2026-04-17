# 导入第三方库
import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

# 读取系统中的环境变量
_ = load_dotenv(find_dotenv())

# 创建 OpenAI API 客户端
client = OpenAI(
        api_key=os.getenv("SILICONFLOW_API_KEY"), # 如果您没有配置环境变量，请在此处用您的API Key进行替换
        base_url="https://api.siliconflow.cn/v1",  # 填写DashScope SDK的base_url
    )

# 一个封装 OpenAI 接口的函数，参数为 Prompt，返回对应结果
def get_completion(prompt, model="Qwen/Qwen2.5-7B-Instruct"):# plus-2024-09-19 plus-2024-08-06
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0, # 模型输出的温度系数，控制输出的随机程度
    )
    return response.choices[0].message.content

text = f"""
我今天从超市买了好多东西，有白花花的大米，花生和面粉，\
还有红红的西红柿，胡萝卜，绿油油的菠菜，以及一些肉。
"""
prompt1 = f"""
请将下列描述中的食物选取出来，如果该食物的种类为蔬菜，则按照顺序输出，对每一种蔬菜输出一行如下信息：
XXX真美味！
其中，XXX为蔬菜的不带特性描述的名称。
如果该蔬菜有颜色描述，在行尾添加：颜色：YYY，其中YYY为颜色的名称

<<<{text}>>>
"""

prompt2 = f"""
请将下列描述中的食物选取出来，如果该食物的种类为蔬菜，则按照顺序输出，对每一种蔬菜仅输出一行如下信息：
XXX真美味！

其中，XXX为蔬菜的不带特性描述的名称。
如果该种蔬菜在原文中有颜色描述，在行尾添加：颜色：YYY，其中YYY为颜色的名称。
如果该种蔬菜在原文中没有颜色描述，则不要在行尾添加颜色信息。

原文:
<<<{text}>>>
"""

prompt3 = f"""
请将下列描述中的食物选取出来，如果该食物的种类为蔬菜，则按照顺序输出，对每一种蔬菜仅输出一行如下信息：
XXX真美味！

其中，XXX为蔬菜的不带特性描述的名称。
如果该种蔬菜在原文中有颜色描述，在行尾添加：颜色：YYY，其中YYY为颜色的名称。
如果该种蔬菜在原文中没有颜色描述，则不要在行尾添加颜色信息。

例如：
原文中包含“绿油油的黄瓜”，则输出：黄瓜真美味！颜色：绿色

原文:
<<<{text}>>>
"""

prompt4 = f"""
请将下列描述中的食物选取出来，如果该食物的种类为蔬菜，则按照顺序输出，对每一种蔬菜仅输出一行如下信息：
XXX真美味！

其中，XXX为蔬菜的不带特性描述的名称。
如果该种蔬菜在原文中有颜色描述，在行尾添加：颜色：YYY，其中YYY为颜色的名称。
如果该种蔬菜在原文中没有颜色描述，则不要在行尾添加颜色信息。

例如：
原文中包含“绿油油的黄瓜”，则输出：黄瓜真美味！颜色：绿色
原文中包含“丝瓜”但没有颜色描述，则输出：丝瓜真美味！

原文:
<<<{text}>>>
"""

prompt4 = f"""
请将下列描述中的食物选取出来，如果该食物的种类为蔬菜，则按照顺序输出，对每一种蔬菜仅输出一行如下信息：
XXX真美味！

其中，XXX为蔬菜的不带特性描述的名称。
在你输出之前，对原文使用"，"进行断句，然后每个断完句子中的蔬菜检查前面是否有颜色，再进行输出
如果该种蔬菜在原文中有颜色描述，在行尾添加：颜色：YYY，其中YYY为颜色的名称。
如果该种蔬菜在原文中没有颜色描述，则不要在行尾添加颜色信息。

例如：
原文中包含“绿油油的黄瓜”，则输出：黄瓜真美味！颜色：绿色
原文中包含“丝瓜”但没有颜色描述，则输出：丝瓜真美味！


原文:
<<<{text}>>>
"""

prompt = prompt3
response = get_completion(prompt)

print(response)
