from llm_client import invoke_messages, invoke_text


def rewrite_steps_demo() -> None:
    text = """
泡一杯茶很容易。首先，需要把水烧开。
在等待期间，拿一个杯子并把茶包放进去。
一旦水足够热，就把它倒在茶包上。
等待一会儿，让茶叶浸泡。几分钟后，取出茶包。
如果你愿意，可以加一点糖或牛奶调味。
就这样，你可以享用一杯美味的茶了。
""".strip()

    prompt = f"""
你将获得一段文本，文本放在三个双引号中。
如果它描述了一系列步骤，请改写成清晰的编号步骤。
如果它不是步骤说明，就只输出“未提供步骤”。

文本：
\"\"\"{text}\"\"\"
""".strip()

    response = invoke_text(prompt, temperature=0)
    print("============= Rewrite Steps Demo =============")
    print(response)


def reasoning_demo() -> None:
    messages = [
        {
            "role": "system",
            "content": "你是数学老师。请用简洁中文回答，并确保最后一行明确写出“最终答案：...”。",
        },
        {
            "role": "user",
            "content": (
                "请按“问题理解、解题步骤、最终答案”三个部分作答。\n"
                "问题：一个班有 48 名学生，其中 3/4 参加了数学竞赛，"
                "参加竞赛的学生里有 2/3 获奖。获奖学生有多少人？"
            ),
        },
    ]

    response = invoke_messages(messages, temperature=0)
    print("============= Reasoning Demo =============")
    print(response)


if __name__ == "__main__":
    rewrite_steps_demo()
    print()
    reasoning_demo()
