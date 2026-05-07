from llm_client import invoke_messages


def main() -> None:
    messages = [
        {
            "role": "system",
            "content": "你是一个乐于助人的 AI 助手，你的名字叫宋朝知识小助手。",
        },
        {"role": "user", "content": "给我讲一个有关岳飞的小故事。"},
    ]

    response = invoke_messages(
        messages,
        model="Qwen/Qwen2.5-7B-Instruct",
        temperature=0.4,
    )
    print("response.content:----------------------")
    print(response)


if __name__ == "__main__":
    main()
