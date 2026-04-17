from langchain_openai import ChatOpenAI

from dotenv import load_dotenv, find_dotenv
import os

_ = load_dotenv(find_dotenv()) 

os.environ["http_proxy"]="http://localhost:7890"
os.environ["https_proxy"]="http://localhost:7890"

model = ChatOpenAI(model="gpt-3.5-turbo")

print(model.invoke("Hello, Langchain!").content)