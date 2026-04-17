from langchain_community.llms.vllm import VLLMOpenAI

model = VLLMOpenAI(openai_api_base="http://10.107.0.80:8080/v1",
                 openai_api_key="NOPWD",
                 model_name="qwen2-72b-int4",
                 max_tokens=2000)

responses = model.stream("请以我爱祖国为题目，写一篇1800字的作文")
for partial in responses:
    print(partial,end="")