import os
from openai import OpenAI

from dotenv import load_dotenv, find_dotenv

# 从 .env 文件中加载 OPENAI_API_KEY
if not load_dotenv(find_dotenv()):
    print("无法加载 .env 文件。")

# 创建 OpenAI API 客户端
client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"), # 如果您没有配置环境变量，请在此处用您的API Key进行替换
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope SDK的base_url
    )


# 从 OpenAI API 获取 LLM 生成的结果
def get_completion_from_messages(messages, model="qwen-plus", temperature=0, max_tokens=1024):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content


# 构造用户消息对象
def generate_user_message(user_input):
    return {"role": "user", "content": user_input}

# 构造系统消息对象
def generate_system_message(system_output):
    return {"role": "system", "content": system_output}

# 构造助手消息对象
def generate_assistant_message(assistant_output):
    return {"role": "assistant", "content": assistant_output}


# 使用不完整的上下文，获取 LLM 的回复
def chat_using_incomplete_context():
    message_system = generate_system_message("你是一个聊天机器人，能回答用户的问题。")

    message_user_1 = generate_user_message("嗨，我是周老师。")
    response_1 = get_completion_from_messages(messages=[message_system, message_user_1])
    print("response_1:",response_1)

    message_user_2 = generate_user_message("好的，你可以提醒我，我的名字是什么吗？")
    response_2 = get_completion_from_messages(messages=[message_system, message_user_2])
    print("response_2:",response_2)

# chat_using_incomplete_context()

# 使用完整的上下文，获取 LLM 的回复
def chat_using_complete_context():
    message_system = generate_system_message("你是一个聊天机器人，能回答用户的问题。")

    message_user_1 = generate_user_message("嗨，我是渠老师。")
    response_1 = get_completion_from_messages(messages=[message_system, message_user_1])
    print("response_1:",response_1)

    message_assistant_1 = generate_assistant_message(response_1)

    message_user_2 = generate_user_message("好的，你可以提醒我，我的名字是什么吗？")
    response_2 = get_completion_from_messages(messages=[
        message_system, message_user_1, message_assistant_1, message_user_2
    ])
    print("response_2:",response_2)

chat_using_complete_context()
