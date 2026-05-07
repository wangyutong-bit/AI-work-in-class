from llm_client import invoke_text


def main() -> None:
    response = invoke_text(
        "你是一名宋朝知识小助手，请列举 5 位宋朝著名诗人的名字。",
        model="gpt-3.5-turbo",
        temperature=0.3,
    )
    print(response)


if __name__ == "__main__":
    main()
