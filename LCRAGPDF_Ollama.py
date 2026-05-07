# pip install langchain_community -i https://mirrors.aliyun.com/pypi/simple/
# pip install langchain_chroma -i https://mirrors.aliyun.com/pypi/simple/
# pip install faiss-cpu -i https://mirrors.aliyun.com/pypi/simple/  
# pip install pypdf -i https://mirrors.aliyun.com/pypi/simple/
import os
import warnings

import bs4

from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader


warnings.filterwarnings('ignore')

model = ChatOllama(model="qwen2:7b")
# Load, chunk and index the contents of the blog.
# 目标文件名
file_name = "20大报告原文.pdf"

# 获取当前目录
current_directory = os.getcwd()
print(f"Current directory: {current_directory}")

# 构建文件路径
file_path = os.path.join(current_directory, file_name)
print(f"File path: {file_path}")

# 确认文件是否存在
if os.path.exists(file_path):
    print("File exists.")
else:
    print("File does not exist.")



loader = PyPDFLoader(file_path)

docs = loader.load()

print("Loader:=================================================")
print("len(docs)",len(docs))
print(len(docs[0].page_content))
print(docs[0].page_content[:500])


print("Split:=================================================")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
splits = text_splitter.split_documents(docs)
print("len(splits):",len(splits))
print("len(splits[10].page_content):",len(splits[10].page_content))
print("splits[10].metadata",splits[10].metadata)


print("Store:=================================================")
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
# vectorstore = FAISS.from_documents(documents=splits, embedding=OpenAIEmbeddings())

print("Retrieve:=================================================")
# Retrieve and generate using the relevant snippets of the blog.
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})
retrieved_docs = retriever.invoke("如何办好人民满意的教育？")

print("len(retrieved_docs)",len(retrieved_docs))
print("retrieved_docs[0].page_content",retrieved_docs[0].page_content)
print("-------------------------------")
print("retrieved_docs[1].page_content",retrieved_docs[1].page_content)
print("-------------------------------")
print("retrieved_docs[2].page_content",retrieved_docs[2].page_content)
print("-------------------------------")
print("retrieved_docs[3].page_content",retrieved_docs[3].page_content)
print("-------------------------------")
print("retrieved_docs[4].page_content",retrieved_docs[4].page_content)
print("-------------------------------")
print("retrieved_docs[5].page_content",retrieved_docs[5].page_content)


print("Generate:=================================================")
system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "input": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

response = rag_chain.invoke("如何办好人民满意的教育？")

print(response)