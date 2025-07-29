import streamlit as st
import os
import pyttsx3
import shutil
from agents.ingestion_agent import IngestionAgent
from agents.retrieval_agent import RetrievalAgent
from agents.llm_response_agent import LLMResponseAgent

# -------------------- VOICE GREETING --------------------
def speak_welcome():
    engine = pyttsx3.init()
    engine.say("Welcome to Agentic Chatbot for Multi-format Document QA")
    engine.runAndWait()

if "welcomed" not in st.session_state:
    speak_welcome()
    st.session_state.welcomed = True

# -------------------- PAGE SETUP --------------------
st.set_page_config(page_title="Agentic RAG Chatbot", layout="centered")
st.title("🤖 Agentic RAG Chatbot")

# -------------------- RESET --------------------
if st.button("🔄 Reset"):
    if os.path.exists("data"):
        shutil.rmtree("data")
    st.session_state.clear()
    st.success("Chat and uploaded files have been reset.")

# -------------------- FILE UPLOAD --------------------
st.header("📤 Upload Your Documents")
uploaded_files = st.file_uploader(
    "Upload PDF, DOCX, PPTX, CSV, or TXT files",
    type=["pdf", "docx", "pptx", "csv", "txt"],
    accept_multiple_files=True
)

if uploaded_files:
    os.makedirs("data", exist_ok=True)
    for file in uploaded_files:
        file_path = os.path.join("data", file.name)
        with open(file_path, "wb") as f:
            f.write(file.read())
    st.success("✅ Files uploaded successfully!")

# -------------------- ASK A QUESTION --------------------
st.header("💬 Ask a Question")
query = st.text_input("Type your question here:")

if st.button("Get Answer"):
    if not query:
        st.warning("Please enter a question.")
    else:
        with st.spinner("🧠 Processing..."):
            # Step 1: Ingest
            ingestion = IngestionAgent()
            ingestion_msg = ingestion.ingest()

            # Step 2: Retrieve
            retrieval = RetrievalAgent()
            retrieval.process_documents(ingestion_msg)
            retrieved_msg = retrieval.retrieve(query)

            # Step 3: Generate Response
            llm = LLMResponseAgent()
            response = llm.generate_response(retrieved_msg)

            # -------------------- OUTPUT --------------------
            st.subheader("💡 Answer:")
            st.success(response["payload"]["answer"])

            st.subheader("📄 Source Context:")
            for chunk in response["payload"]["full_context"]:
                st.markdown(f"- {chunk}")
