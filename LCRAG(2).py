# pip install langchain_community -i https://mirrors.aliyun.com/pypi/simple/
# pip install langchain_chroma -i https://mirrors.aliyun.com/pypi/simple/
# pip install faiss-cpu -i https://mirrors.aliyun.com/pypi/simple/  
# pip install beautifulsoup4 -i https://mirrors.aliyun.com/pypi/simple/
import os
import warnings

import bs4

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_community.vectorstores.faiss import FAISS
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import DashScopeEmbeddings

from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv()) 

warnings.filterwarnings('ignore')

# Load, chunk and index the contents of the blog.
loader = WebBaseLoader(
    web_paths=("https://www.gov.cn/xinwen/2022-10/25/content_5721685.htm",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("pages_content")
        )
    ),
)
docs = loader.load()

print("Loader:=================================================")
print("len(docs):  ",len(docs))
print(len(docs[0].page_content))
print(docs[0].page_content[:500])


print("Split:=================================================")
text_splitter = RecursiveCharacterTextSplitter(length_function=len, chunk_size=1000, chunk_overlap=200,add_start_index=True)
splits = text_splitter.split_documents(docs)
print("len(splits):",len(splits))
print("len(splits[9].page_content):",len(splits[9].page_content))
print("splits[9].page_content:",splits[9].page_content)
print("splits[9].metadata",splits[9].metadata)
print("=================================================")
print("len(splits[10].page_content):",len(splits[10].page_content))
print("splits[10].page_content:",splits[10].page_content)

print("Store:=================================================")
# vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings(
#     model="BAAI/bge-m3",
#     base_url="https://api.siliconflow.cn/v1",
#     api_key=os.getenv("SILICONCLOUD_API_KEY")
# ))
dashscope_embedding = DashScopeEmbeddings(
    model="text-embedding-v2", 
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
)
vectorstore = Chroma.from_documents(documents=splits, embedding=dashscope_embedding)
# vectorstore = FAISS.from_documents(documents=splits, embedding=dashscope_embedding)


print("Retrieve:=================================================")
# Retrieve and generate using the relevant snippets of the blog.
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 4})
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
# print("retrieved_docs[4].page_content",retrieved_docs[4].page_content)
# print("-------------------------------")
# print("retrieved_docs[5].page_content",retrieved_docs[5].page_content)
# print("-------------------------------")
# print("retrieved_docs[6].page_content",retrieved_docs[6].page_content)
# print("-------------------------------")
# print("retrieved_docs[7].page_content",retrieved_docs[7].page_content)


print("Generate:=================================================")
model = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-plus")

system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use eight sentences maximum and keep the "
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