import os
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template

load_dotenv()

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text 

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len
    )
    chunks = text_splitter.split_text(text);
    return chunks

# Function to create Chroma vector store using Gemini embeddings
def get_vectorstore(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(
        model = "models/embedding-001",
        google_api_key = os.getenv("GEMINI_API_KEY")
    )
    vectorstore = Chroma.from_texts(
        texts = text_chunks,
        embedding = embeddings,
        persist_directory = "chroma_db"
    )
    return vectorstore

# function to create chat chain using gemini
def get_conversation_chain(vectorstore):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key = os.getenv("GEMINI_API_KEY"),
        temperature = 0.3
    )

    memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True
    )

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever = vectorstore.as_retriever(),
        memory = memory
    )

    return conversation_chain

# handles user questions
def handle_userinput(user_question):
    response = st.session_state.conversation({
        'question' : user_question
    })
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else: 
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

def main():

    st.set_page_config(
        page_title="Chat with multiple PDFs",
        page_icon=":books:",
    )
    st.write(css, unsafe_allow_html = True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs")
    user_question = st.text_input("Ask a question about your Documents:")

    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("your docments")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)

        if st.button("Process"):
            with st.spinner("Processing..."):
                # Clear old conversation + memory
                st.session_state.chat_history = []
                st.session_state.conversation = None
            #get the pdfs text
                raw_text = get_pdf_text(pdf_docs)
    
            #get the text chunks
                text_chunks = get_text_chunks(raw_text)

            #create the vectorstore
                vector_store = get_vectorstore(text_chunks)
                st.write(vector_store)
            # create gemini based chat system
            st.session_state.conversation = get_conversation_chain(vector_store)
            st.success("Processing Complete!")

if __name__ == "__main__":
    main()
