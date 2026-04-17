import os
import json

from alibabacloud_green20220302.client import Client
from alibabacloud_green20220302 import models
from alibabacloud_tea_openapi.models import Config

from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

# 从 .env 文件中加载 OPENAI_API_KEY
if not load_dotenv(find_dotenv()):
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
def get_completion_from_messages(messages, model="Qwen/Qwen2.5-7B-Instruct", temperature=0.8, max_tokens=1024):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content


# 0. 假设 LLM 的输出结果如下：
final_response = f"""\
您好！很高兴为您介绍这些产品：

1. **SmartX Pro 手机**：这是一款功能强大的智能手机，拥有6.1英寸显示屏、128GB存储空间、1200万像素双摄像头和5G网络支持，非常适合追求高性能和优质摄影体验的用户。售价为$899.99。

2. **FotoSnap 单反相机**：这款相机配备2420万像素传感器、1080p视频录制能力和3英寸液晶屏，支持更换镜头，是摄影爱好者的理想选择。售价为$599.99。

3. **CineView 电视系列**：
   - **4K 电视 (CV-4K55)**：55英寸4K分辨率，支持HDR技术，内置智能系统，售价$599.99。
   - **8K 电视 (CV-8K65)**：65英寸8K超高清屏幕，同样支持HDR和智能功能，带来极致视觉 享受，售价$2999.99。
   - **OLED 电视 (CV-OLED55)**：55英寸OLED屏幕，提供出色的色彩对比度和深黑色表现，同样具备智能功能，售价$1499.99。

您对哪款产品感兴趣？需要了解更多细节或帮助吗？
"""

# 1. 使用 文本审查接口 审查 LLM 的输出

moderation_response = get_llm_output_moderation_response(final_response)
print("moderation_response:-----------------------------")
print(moderation_response)


# 用户输入的内容
user_input = "请告诉我关于 SmartX Pro 手机和 FotoSnap 相机，单反那款。另外，也介绍一下你们的电视。"
# user_input = "我的路由器坏了"


product_detail = """\
{
    "name": "SmartX Pro手机",
    "category": "智能手机和配件",
    "brand": "SmartX",
    "model_number": "SX-PP10",
    "warranty": "1年",
    "rating": 4.6,
    "features": [
        "6.1英寸显示屏",
        "128GB存储",
        "1200万像素双摄像头",
        "5G"
    ],
    "description": "一款功能强大的智能手机，具备先进的摄像功能。",
    "price": 899.99
}
{
    "name": "FotoSnap 单反相机",
    "category": "相机和摄像机",
    "brand": "FotoSnap",
    "model_number": "FS-DSLR200",
    "warranty": "1年保修",
    "rating": 4.7,
    "features": [
        "2420万像素传感器",
        "1080p视频",
        "3英寸液晶屏",
        "可更换镜头"
    ],
    "description": "用这款多功能单反相机捕捉令人惊叹的照片和视频。",
    "price": 599.99
}
{
    "name": "CineView 4K 电视",
    "category": "电视和家庭影院系统",
    "brand": "CineView",
    "model_number": "CV-4K55",
    "warranty": "2年",
    "rating": 4.8,
    "features": [
        "55英寸显示屏",
        "4K分辨率",
        "HDR",
        "智能电视"
    ],
    "description": "一台具有鲜艳色彩和智能功能的出色4K电视。",
    "price": 599.99
}
{
    "name": "CineView 8K 电视",
    "category": "电视和家庭影院系统",
    "brand": "CineView",
    "model_number": "CV-8K65",
    "warranty": "2年",
    "rating": 4.9,
    "features": [
        "65英寸显示屏",
        "8K分辨率",
        "HDR",
        "智能电视"
    ],
    "description": "用这款令人惊艳的8K电视体验电视的未来。",
    "price": 2999.99
}
{
    "name": "CineView OLED电视",
    "category": "电视和家庭影院系统",
    "brand": "CineView",
    "model_number": "CV-OLED55",
    "warranty": "2年保修",
    "rating": 4.7,
    "features": [
        "55英寸屏幕",
        "4K分辨率",
        "HDR",
        "智能电视"
    ],
    "description": "用这款OLED电视体验真正的深黑和鲜艳的色彩。",
    "price": 1499.99
}
"""


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
