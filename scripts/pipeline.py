import bs4
from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import Docx2txtLoader
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import sys
sys.path.insert(1, '/home/jabez/week_11/Contract-Advisor-RAG/scripts/data_processing.py')
load_dotenv()

def chatbot(vectorstore, question):
    retriever = vectorstore.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")

    llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)


    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    answer = rag_chain.invoke(question)
    return answer 