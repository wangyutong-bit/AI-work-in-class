from zhipuai import ZhipuAI

# 你的 API Key
API_KEY = "7750edd425154cc6a024c788f914471e.9Z4kZaJij7a49Xeb"

client = ZhipuAI(api_key=API_KEY)

# 初始化对话历史
messages = [
    {"role": "system", "content": "你是一个助手。"}
]

while True:
    # 获取用户输入 (去掉末尾可能自带的换行符，防止干扰)
    try:
        user_input = input()
    except EOFError:
        break

    if user_input.lower() in ['quit', 'exit']:
        break

    if not user_input.strip():
        continue

    messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="glm-4-flash",
            messages=messages,
            stream=True
        )

        full_response = ""

        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content


                print(content, end="", flush=True)

                full_response += content

        if not full_response.endswith('\n'):
            print()

        messages.append({"role": "assistant", "content": full_response})

    except Exception as e:
        print(f"\nError: {e}")
        messages.pop()