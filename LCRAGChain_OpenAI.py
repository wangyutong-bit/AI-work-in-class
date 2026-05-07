# pip install langchain_community -i https://mirrors.aliyun.com/pypi/simple/
# pip install langchain_chroma -i https://mirrors.aliyun.com/pypi/simple/
# pip install faiss-cpu -i https://mirrors.aliyun.com/pypi/simple/  
import os
import warnings

import bs4

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_community.vectorstores.faiss import FAISS
from langchain_community.document_loaders import WebBaseLoader

from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv()) 

os.environ["http_proxy"]="http://localhost:7890"
os.environ["https_proxy"]="http://localhost:7890"

warnings.filterwarnings('ignore')

model = ChatOpenAI(model="gpt-3.5-turbo")

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
print("len(docs)",len(docs))
print(len(docs[0].page_content))
print(docs[0].page_content[:500])


print("Split:=================================================")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
print("len(splits):",len(splits))
print("len(splits[10].page_content):",len(splits[10].page_content))
print("splits[10].metadata",splits[10].metadata)


print("Store:=================================================")
# vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
vectorstore = FAISS.from_documents(documents=splits, embedding=OpenAIEmbeddings())

print("Retrieve:=================================================")
# Retrieve and generate using the relevant snippets of the blog.
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 4})
retrieved_docs = retriever.invoke("如何建设现代化产业体系？")

print("len(retrieved_docs)",len(retrieved_docs))
print("retrieved_docs[0].page_content",retrieved_docs[0].page_content)
print("-------------------------------")
print("retrieved_docs[1].page_content",retrieved_docs[1].page_content)
print("-------------------------------")
print("retrieved_docs[2].page_content",retrieved_docs[2].page_content)
print("-------------------------------")
print("retrieved_docs[3].page_content",retrieved_docs[3].page_content)
# print("-------------------------------")
# print("retrieved_docs[4].page_content",retrieved_docs[4].page_content)
# print("-------------------------------")
# print("retrieved_docs[5].page_content",retrieved_docs[5].page_content)


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

question_answer_chain = create_stuff_documents_chain(model, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

response = rag_chain.invoke({"input": "如何建设现代化产业体系？"})

print(response["answer"])