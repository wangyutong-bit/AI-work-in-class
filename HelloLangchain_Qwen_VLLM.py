from llm_client import invoke_text


def main() -> None:
    response = invoke_text(
        "请以“我爱祖国”为题，写一篇 800 字左右的作文。",
        model="qwen2-72b-int4",
        base_url="http://10.107.0.80:8080/v1",
        api_key="NOPWD",
        temperature=0.7,
        max_tokens=2000,
    )
    print(response)


if __name__ == "__main__":
    main()
