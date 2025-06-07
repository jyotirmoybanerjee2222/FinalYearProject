import streamlit as st
import os
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai

os.environ["GOOGLE_API_KEY"] = "Paste your Google api key"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

@st.cache_resource
def load_vectorstore(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    return FAISS.from_texts(text_chunks, embeddings)

def get_gemini_response(prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

def run_qna():
    st.title("💬 PDF QnA Chatbot")

    pdf = st.file_uploader("Upload a PDF", type="pdf")

    if pdf:
        reader = PdfReader(pdf)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

        st.success("PDF Loaded.")

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_text(text)
        vectorstore = load_vectorstore(chunks)

        query = st.text_input("Ask a question about the PDF:")

        if query:
            docs = vectorstore.similarity_search(query, k=3)
            context = "\n\n".join([doc.page_content for doc in docs])
            prompt = f"Based on the following PDF content:\n\n{context}\n\nAnswer this question:\n{query}"
            answer = get_gemini_response(prompt)
            st.write("📌 Answer:", answer)
