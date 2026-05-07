from llm_client import invoke_text


def main() -> None:
    response = invoke_text(
        "你好，请用一句中文介绍一下大语言模型应用开发。",
        model="gpt-3.5-turbo",
        temperature=0.3,
    )
    print(response)


if __name__ == "__main__":
    main()
