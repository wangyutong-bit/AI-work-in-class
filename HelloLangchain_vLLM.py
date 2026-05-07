from llm_client import invoke_text


def main() -> None:
    response = invoke_text(
        "你好，介绍一下 LangChain 的几个核心模块。",
        model="Qwen2.5-7B-AIGCCLASS",
        base_url="http://127.0.0.1:6006/v1",
        api_key="i_am_api_key",
        temperature=0.3,
        max_tokens=800,
    )
    print(response)


if __name__ == "__main__":
    main()
