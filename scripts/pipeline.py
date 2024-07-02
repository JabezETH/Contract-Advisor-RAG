import sys
import os
from dotenv import load_dotenv
from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader, Docx2txtLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate

sys.path.insert(1, '/home/jabez/week_11/Contract-Advisor-RAG/scripts/data_processing.py')
load_dotenv()

def chatbot(vectorstore, question):
    retriever = vectorstore.as_retriever()
    
    # Define the prompt template
    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="""
        Use the following context to answer the question. Do not use any outside knowledge. If the answer is not in the context, simply state "The information is not available in the provided context."

        Context:
        {context}

        Question:
        {question}

        Answer:
        """
    )
    
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # Define the chain with the prompt template
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | RunnableLambda(lambda inputs: prompt_template.format(**inputs))
        | llm
        | StrOutputParser()
    )

    answer = rag_chain.invoke(question)
    return answer