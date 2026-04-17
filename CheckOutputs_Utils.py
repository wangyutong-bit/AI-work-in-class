import os
import json

from alibabacloud_green20220302.client import Client
from alibabacloud_green20220302 import models
from alibabacloud_tea_openapi.models import Config

from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

from ChainingPrompt import (
    find_products_and_category, 
    get_products_string,
    get_final_response 
)

# 从 .env 文件中加载 OPENAI_API_KEY
if not load_dotenv(find_dotenv(r"C:\Users\Ninler\Desktop\AI-test\.env")):
    print("无法加载 .env 文件。")


# 配置阿里云账号信息
config = Config(
    access_key_id=os.environ["ALIBABA_CLOUD_ACCESS_KEY_ID"],         # 阿里云账号 AccessKey ID
    access_key_secret=os.environ["ALIBABA_CLOUD_ACCESS_KEY_SECRET"], # 阿里云账号 AccessKey Secret
    connect_timeout=10000,
    read_timeout=3000,
    region_id='cn-hangzhou',
    endpoint='green-cip.cn-hangzhou.aliyuncs.com'
)

# 创建用于访问阿里云内容审查服务的客户端
green_client = Client(config)

# 定义函数，用于访问 阿里云 面向大语言模型的文本审核 PLUS 服务
def get_llm_output_moderation_response(model_output):
    # 构建请求对象，调用阿里云内容审查服务
    request = models.TextModerationPlusRequest(
        service="llm_response_moderation", # 用于审核用户输入给 LLM 的文本
        service_parameters=json.dumps({
            'content': model_output
        }),
    )
    try:
        response = green_client.text_moderation_plus(request)
        if response.status_code != 200:
            raise RuntimeError
        return response.body
    except Exception:
        return None


# 创建 OpenAI API 客户端（调用通义千问 API）
client = OpenAI(
        api_key=os.getenv("SILICONFLOW_API_KEY"), # 如果您没有配置环境变量，请在此处用您的API Key进行替换
        base_url="https://api.siliconflow.cn/v1",  # 填写DashScope SDK的base_url
    )

# 从 OpenAI API 获取 LLM 生成的结果
def get_completion_from_messages(messages, model="Qwen/Qwen2.5-7B-Instruct", temperature=0,max_tokens=2048):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content

# 用户输入的内容
user_input = "请告诉我关于 SmartX Pro 手机和 FotoSnap 相机，单反那款。另外，也介绍一下你们的电视。"
# user_input = "我的路由器坏了"

# 0. 假设 LLM 的输出结果如下：
product_names = find_products_and_category(user_input)
product_detail = get_products_string(product_names)
final_response = get_final_response(user_input,product_detail)

# 1. 使用 文本审查接口 审查 LLM 的输出
moderation_response = get_llm_output_moderation_response(final_response)
print("moderation_response:-----------------------------")
print(moderation_response)


# 2. 使用 LLM 判断输出结果是否符合预期
system_message = f"""\
你是一个助手，负责检查智能客服的回复是否解答了用户的问题，\
同时还需要检查助手引用的所有产品信息是否准确。\
产品信息、用户输入和智能客服的回复将以以下格式给出：
user: ```<用户输入>```
assistant: ```<智能客服的回复>```
products: ```<产品信息>```

你只能使用 Y 或 N 来输出你的判断
Y - 智能客服的回复充分回答了问题，且回复中正确使用了产品信息
N - 其他情况
"""
question_input = f"""\
user: ```{user_input}```
assistant: ```{final_response}```
products: ```{product_detail}```
"""

# 使用 LLM 判断输出质量
response = get_completion_from_messages(messages=[
    { "role": "system", "content": system_message },
    { "role": "user", "content": question_input }
], max_tokens=1)
print(response)
