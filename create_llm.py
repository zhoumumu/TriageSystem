from dotenv import load_dotenv
load_dotenv()
import os
print(os.getenv('OPENAI_BASE_URL'))
from langchain_openai import ChatOpenAI

#Available models in Ali:
# deepseek-v3 ×: function calling not supported
# deepseek-r1-distill-llama-70b
# deepseek-r1-distill-qwen-32b
# deepseek-r1-distill-qwen-14b
# deepseek-r1-distill-llama-8b ×: function calling not supported
# deepseek-r1-distill-qwen-1.5b
# deepseek-r1-distill-qwen-7b
# deepseek-r1 ×: function calling not supported
# qwen2.5-14b-instruct ×
# qwen2.5-32b-instruct √
# qwen2.5-72b-instruct √
# qwen2.5-coder-32b-instruct ×
# qwen2.5-math-72b-instruct ×: bad output, short input_len
# qwen-72b-chat ×
# qwen-14b-chat ×
# qwen-long
# qwen-max-longcontext
# qwen-max
# qwen-turbo
# qwen-plus √
llm = ChatOpenAI(model="qwen-plus", temperature=0.2)
llm_2 = ChatOpenAI(model="gpt-4o-mini", api_key="sk-lthXPzxwZR2FKBIqgDKn7zwbnp7U9YMYJtoGqYE0C0bW3mt0", base_url="https://one-api.boolv.tech/v1")
