from llm_client import invoke_text


def main() -> None:
    response = invoke_text(
        "你好，如何实现 LangChain 的链式调用？请用中文简要说明。",
        model="qwen2Qwen2.5-7B-Instruct-AIGCCLASS-SFT",
        base_url="http://0.0.0.0:8000/v1",
        api_key="no_api_key",
        temperature=0.3,
        max_tokens=800,
    )
    print(response)


if __name__ == "__main__":
    main()
