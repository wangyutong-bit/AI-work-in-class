import os
import json

from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

# 从 .env 文件中加载 OPENAI_API_KEY
if not load_dotenv(find_dotenv()):
    print("无法加载 .env 文件。")

# 创建 OpenAI API 客户端
client = OpenAI(
        api_key=os.getenv("SILICONFLOW_API_KEY"), # 如果您没有配置环境变量，请在此处用您的API Key进行替换
        base_url="https://api.siliconflow.cn/v1",  # 填写DashScope SDK的base_url
    )


# 从 OpenAI API 获取 LLM 生成的结果
def get_completion_from_messages(messages, model="Qwen/Qwen2.5-7B-Instruct", temperature=0, max_tokens=1024):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content


delimiter = "######"
system_message = f"""\
按照以下步骤回答用户的问题：
客户的询问将使用以下字符串进行分隔：{delimiter}

步骤1：首先确定用户是否在询问特定产品或多个产品的问题，不用考虑产品的分类。

步骤2：如果用户询问特定的产品，请确定这些产品是否在以下列表中：
所有的产品包括以下列表：
1. 产品：TechPro Ultrabook
   类别：电脑和笔记本电脑
   品牌：TechPro
   型号：TP-UB100
   保修期：1年
   评分：4.5
   特点：13.3英寸显示屏，8GB RAM，256GB SSD，Intel Core i5处理器
   描述：一款轻薄、适合日常使用的超级笔记本。
   价格：$799.99

2. 产品：BlueWave 游戏笔记本
   类别：电脑和笔记本电脑
   品牌：BlueWave
   型号：BW-GL200
   保修期：2年
   评分：4.7
   特点：15.6英寸显示屏，16GB RAM，512GB SSD，NVIDIA GeForce RTX 3060
   描述：一款高性能的游戏笔记本，为您提供沉浸式体验。
   价格：$1199.99

3. 产品：PowerLite 可翻转笔记本
   类别：电脑和笔记本电脑
   品牌：PowerLite
   型号：PL-CV300
   保修期：1年
   评分：4.3
   特点：14英寸触摸屏，8GB RAM，256GB SSD，360度转轴
   描述：一款多功能可转换笔记本，配有敏捷的触摸屏。
   价格：$699.99

4. 产品：TechPro 台式电脑
   类别：电脑和笔记本电脑
   品牌：TechPro
   型号：TP-DT500
   保修期：1年
   评分：4.4
   特点：Intel Core i7处理器，16GB RAM，1TB HDD，NVIDIA GeForce GTX 1660
   描述：一款适用于工作和娱乐的强大台式电脑。
   价格：$999.99

5. 产品：BlueWave Chromebook
   类别：电脑和笔记本电脑
   品牌：BlueWave
   型号：BW-CB100
   保修期：1年
   评分：4.1
   特点：11.6英寸显示屏，4GB RAM，32GB eMMC，Chrome OS
   描述：一款紧凑且价格实惠的Chromebook，适用于日常任务。
   价格：$249.99

步骤3：如果用户信息中包含上述列表中的产品，请列出用户在对其询问中做出任何的假设，例如笔记本电脑X比笔记本电脑Y贵，或者笔记本电脑Z有2年保修期。
步骤4：如果用户做了任何的假设，请根据你的产品信息判断假设是否正确。
步骤5：如果可以的话，请礼貌地纠正用户的错误假设。只提及或引用列表中可用的产品，因为这些产品是商店中唯一可用的产品。这一步的结果可以包含在你的回复中。

注意，需要以友好客气的语气回答用户的问题。

使用以下格式输出内容：
{{
    "steps": {{
       "step_1": "<步骤1的推理>",
       "step_2": "<步骤2的推理>",
       "step_3": "<步骤3的推理>",
       "step_4": "<步骤4的推理>",
       "step_5": "<步骤5的推理>",
    }}
    "response": "<回复用户>"
}}

确保使用上述JSON格式回答，否则你的回答视为无效。
"""


user_input_1 = "BlueWave Chromebook 比 TechPro 台式电脑贵吗？如果更贵，那么它贵多少？"
response_1 = get_completion_from_messages(messages=[
    { "role": "system", "content": system_message },
    { "role": "user", "content": f"{delimiter} {user_input_1} {delimiter}" }
])
print("response_1: -----------------------------------------")
print(response_1)

try:
	# 提取大语言模型中最终输出的回复
	final_answer_1 = json.loads(response_1)['response']
except Exception:
	# 如果大语言模型的回复有问题，告知用户稍后重试
    final_answer_1 = "系统出了一点问题，请稍后再试。"

print(final_answer_1)


user_input_2 = "你们有卖电视吗？"
response_2 = get_completion_from_messages(messages=[
    { "role": "system", "content": system_message },
    { "role": "user", "content": f"{delimiter} {user_input_2} {delimiter}" }
])
print("response_2: -----------------------------------------")
print(response_2)

try:
	# 提取大语言模型中最终输出的回复
	final_answer_2 = json.loads(response_2)['response']
except Exception:
	# 如果大语言模型的回复有问题，告知用户稍后重试
    final_answer_2 = "系统出了一点问题，请稍后再试。"
print(final_answer_2)


user_input_3 = "保修期最长的笔记本电脑是哪个？"
response_3 = get_completion_from_messages(messages=[
    { "role": "system", "content": system_message },
    { "role": "user", "content": f"{delimiter} {user_input_3} {delimiter}" }
])
print("response_3: -----------------------------------------")
print(response_3)

try:
	# 提取大语言模型中最终输出的回复
	final_answer_3 = json.loads(response_3)['response']
except Exception:
	# 如果大语言模型的回复有问题，告知用户稍后重试
    final_answer_3 = "系统出了一点问题，请稍后再试。"
print(final_answer_3)