from llm_client import invoke_messages, invoke_text


def format_chat_messages(template: list[tuple[str, str]], **kwargs: str) -> list[dict[str, str]]:
    role_map = {"system": "system", "human": "user", "ai": "assistant"}
    messages = []
    for role, content in template:
        messages.append({"role": role_map[role], "content": content.format(**kwargs)})
    return messages


def chat_prompt_template_demo() -> None:
    template = [
        ("system", "你是一个乐于助人的 AI 助手，你的名字叫{name}。"),
        ("human", "你好，你正在做什么？"),
        ("ai", "我正在待命，随时准备帮助你。"),
        ("human", "{user_input}"),
    ]

    messages = format_chat_messages(
        template,
        name="学习助手",
        user_input="请先介绍一下你自己，再给我一句学习大模型开发的建议。",
    )

    print("============= Chat Messages =============")
    print(messages)

    response = invoke_messages(messages, temperature=0.3)
    print("============= LLM Response =============")
    print(response)


def translation_demo() -> None:
    prompt = """将下面用三个反引号包裹的文本翻译成直白、现代的中文白话文。
文本: ```三十功名尘与土，八千里路云和月。莫等闲、白了少年头，空悲切。```"""

    print("============= Translation Prompt =============")
    print(prompt)

    response = invoke_text(prompt, temperature=0.2)
    print("============= Translation Result =============")
    print(response)


if __name__ == "__main__":
    chat_prompt_template_demo()
    print()
    translation_demo()
