from llm_client import invoke_text


def main() -> None:
    response = invoke_text("你好，LangChain 是什么？请用中文简要介绍。", temperature=0.3)
    print(response)


if __name__ == "__main__":
    main()
