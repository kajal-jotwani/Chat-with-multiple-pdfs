# 📚 Chat with Multiple PDFs using Gemini + Streamlit

This is a Streamlit app that allows you to upload multiple PDF files, processes them using Google's **Gemini Pro** embeddings, stores them in a **Chroma vector database**, and lets you chat with the content using a conversational AI interface.

---

## 🚀 Features

- 📄 Upload multiple PDF documents
- 🧠 Chat with your documents using Google Gemini Pro
- 💬 Conversation memory for context-aware responses
- 📊 Visual chat interface using custom templates
- 🔍 Retrieves relevant answers from vector-embedded PDF content

---

## 🧰 Tech Stack

- [Streamlit](https://streamlit.io/) — Web app framework
- [LangChain](https://www.langchain.com/) — For LLM chains, memory, and embeddings
- [Google Generative AI (Gemini)](https://ai.google.dev) — Embeddings + Chat model
- [ChromaDB](https://www.trychroma.com/) — Vector database
- [PyPDF2](https://pypi.org/project/PyPDF2/) — PDF text extraction

---

## 🛠️ Setup Instructions

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```
2. **Create a virtual environment**  
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows env\Scripts\activate

   ```
3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your environment variables**  
   ```bash
   GEMINI_API_KEY=your_google_generative_ai_key
    ```

5. **Run the app**  
   ```bash
   streamlit run your_script_name.py
    ```