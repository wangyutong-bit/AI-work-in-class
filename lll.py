from zai import ZhipuAiClient
client = ZhipuAiClient(api_key="7750edd425154cc6a024c788f914471e.9Z4kZaJij7a49Xeb")
# 创建聊天完成请求
response = client.chat.completions.create(
    model="glm-5",
    messages=[
        {
            "role": "system",
            "content": "你是一个有用的AI助手。"
        },
        {
            "role": "user",
            "content": "你好，请介绍一下自己。"
        }
    ],
    temperature=0.6
)

# 获取回复
print(response.choices[0].message.content)