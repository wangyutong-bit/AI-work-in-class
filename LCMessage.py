from dataclasses import dataclass

from llm_client import invoke_messages


@dataclass
class SystemMessage:
    content: str
    type: str = "system"


class SystemMessagePromptTemplate:
    def __init__(self, template: str) -> None:
        self.template = template

    @classmethod
    def from_template(cls, template: str) -> "SystemMessagePromptTemplate":
        return cls(template)

    def format(self, **kwargs: str) -> SystemMessage:
        return SystemMessage(content=self.template.format(**kwargs))


def system_message_demo() -> None:
    system_message = SystemMessage(content="你是一个乐于助人的 AI 助手，你的名字叫宋朝知识小助手。")
    print(type(system_message))
    print(system_message.type)
    print(system_message)
    print("===============================")

    system_message_prompt_template = SystemMessagePromptTemplate.from_template(
        "你好啊，{assigned_role}"
    )
    print(type(system_message_prompt_template))
    print(system_message_prompt_template)

    format_result = system_message_prompt_template.format(assigned_role="宋朝知识小助手！")
    print(type(format_result))
    print(format_result)
    print("===============================")

    response = invoke_messages(
        [
            {"role": "system", "content": system_message.content},
            {"role": "user", "content": "请用一句话介绍你的职责。"},
        ],
        temperature=0.3,
    )
    print("LLM Response:")
    print(response)


if __name__ == "__main__":
    system_message_demo()
