import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()
# Set the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_pdf_text(pdf_docs):
    text = ''
    for pdf_doc in pdf_docs:
        pdf = PdfReader(pdf_doc)
        for page in pdf.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    vectorstore.save_local("faiss_index")
    return vectorstore

def get_conversation_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to providse all the details, 
    if the answer is not in the context, "answer is not available in the context", don't provide wronmg answer.
    Context: \n {context}?\n 
    Question: \n {question}\n

    Answer:
    """
    model=ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template = prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(llm=model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question, k=1)

    chain = get_conversation_chain()
    response = chain({"input_documents": docs, "question": user_question},
                      return_only_outputs=True)
    print(response)
    st.write("Reply: ", response["output_text"])

def main():
    st.set_page_config("Chat with multiple PDFs")
    st.header("Chat with multiple PDFs using Google Gemini")

    user_question = st.text_input("Ask a question about your PDF documents:")

    if(user_question):
        user_input(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload PDF files and click on 'Submit & Process' button", type=["pdf"], accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                text = get_pdf_text(pdf_docs)
                chunks = get_text_chunks(text)
                get_vector_store(chunks)
                st.success("PDFs processed successfully!")

if __name__ == "__main__":
    main()