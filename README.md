# 🤖 Agentic RAG Chatbot - Multi-format Document Q&A

Welcome to the **Agentic RAG Chatbot**, an intelligent chatbot that can read files like PDF, Word, PPT, CSV, or Text and answer your questions from them! It uses the power of AI to understand your documents and give smart, short, and meaningful responses.

---

## 📚 What This Project Does

✅ You upload your documents  
✅ The chatbot reads and stores them  
✅ You ask a question about your files  
✅ The chatbot finds relevant info and answers your query  
✅ All done using AI!

---

## 🧠 How It Works

This chatbot uses a **Retrieval-Augmented Generation (RAG)** pipeline with **agents**:

1. **Ingestion Agent** – Reads your documents  
2. **Retrieval Agent** – Finds the best pieces of text that match your question  
3. **LLM Response Agent** – Uses a Language Model to generate the final answer

---

## 🛠️ Technologies Used

- **Python**
- **Streamlit** – for the web interface
- **Hugging Face Transformers** – for LLM (FLAN-T5)
- **FAISS** – for semantic search
- **SentenceTransformers** – for text embeddings
- **Pyttsx3** – for voice greeting
- **Docx2txt, PyMuPDF, python-pptx, Pandas** – for reading various file types

---

## 📁 Supported File Types

You can upload:
- `.pdf` – PDF documents  
- `.docx` – Word documents  
- `.pptx` – PowerPoint presentations  
- `.csv` – Excel-style tables  
- `.txt` – Plain text files

---

