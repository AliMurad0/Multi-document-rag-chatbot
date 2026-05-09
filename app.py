import os
import base64
import streamlit as st

from utils.loaders import load_documents
from utils.vector_store import create_vector_store

from dotenv import load_dotenv

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from langchain_groq import ChatGroq

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Multi-Document RAG Chatbot",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Multi-Document RAG Chatbot")


# =========================
# SESSION STATE
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "vector_store_created" not in st.session_state:
    st.session_state.vector_store_created = False


# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.header("⚙ Dashboard")

    st.markdown("### Uploaded Files")

    uploaded_files_sidebar = []

    st.markdown("---")

    st.markdown("### Model")
    st.info("llama-3.1-8b-instant")

    st.markdown("### Vector DB")
    if st.session_state.vector_store_created:
        st.success("FAISS Ready")
    else:
        st.warning("No Vector DB Yet")

    st.markdown("---")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# =========================
# FILE UPLOAD
# =========================

uploaded_files = st.file_uploader(
    "Upload PDF, DOCX, TXT",
    accept_multiple_files=True
)

# =========================
# PROCESS DOCUMENTS
# =========================

if uploaded_files:

    with st.spinner("Processing documents..."):

        documents = load_documents(uploaded_files)

        create_vector_store(documents)

        st.session_state.vector_store_created = True

    st.success("Documents processed successfully!")

    # Sidebar File Names
    with st.sidebar:
        for file in uploaded_files:
            st.write(f"📄 {file.name}")


# =========================
# PDF PREVIEW
# =========================

if uploaded_files:

    first_pdf = None

    for file in uploaded_files:
        if file.name.endswith(".pdf"):
            first_pdf = file
            break

    if first_pdf:

        st.markdown("## 📄 PDF Preview")

        base64_pdf = base64.b64encode(first_pdf.read()).decode("utf-8")

        pdf_display = f"""
        <iframe
            src="data:application/pdf;base64,{base64_pdf}"
            width="100%"
            height="500"
            type="application/pdf">
        </iframe>
        """

        st.markdown(pdf_display, unsafe_allow_html=True)


# =========================
# LOAD VECTOR STORE
# =========================

def load_vector_store():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = FAISS.load_local(
        "vector_db",
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vector_store


# =========================
# CUSTOM PROMPT
# =========================

custom_prompt = PromptTemplate(
    template="""
You are an AI assistant.

Answer ONLY from the provided context.

If the answer is not available in the context,
say:
"I could not find this in the uploaded documents."

Provide concise and professional answers.

Context:
{context}

Question:
{question}

Answer:
""",
    input_variables=["context", "question"]
)


# =========================
# CREATE QA CHAIN
# =========================

def get_qa_chain():

    vector_store = load_vector_store()

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 4}
    )

    llm = ChatGroq(
        model_name="llama-3.1-8b-instant",
        temperature=0.3
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={
            "prompt": custom_prompt
        }
    )

    return qa_chain


# =========================
# ACTION BUTTONS
# =========================

st.markdown("## ⚡ Quick Actions")

col1, col2, col3, col4 = st.columns(4)

action_prompt = None

with col1:
    if st.button("📄 Summarize Document"):
        action_prompt = "Summarize the uploaded documents."

with col2:
    if st.button("🔑 Generate Key Points"):
        action_prompt = "Generate important key points from the uploaded documents."

with col3:
    if st.button("🛠 Extract Skills"):
        action_prompt = "Extract all technical skills from the uploaded documents."

with col4:
    if st.button("❓ Generate Quiz"):
        action_prompt = "Generate 5 quiz questions from the uploaded documents."


# =========================
# CHAT INPUT
# =========================

question = st.chat_input("Ask a question from your documents")

if question:
    action_prompt = question


# =========================
# DISPLAY CHAT HISTORY
# =========================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# =========================
# GENERATE RESPONSE
# =========================

if action_prompt and st.session_state.vector_store_created:

    # USER MESSAGE

    st.session_state.messages.append({
        "role": "user",
        "content": action_prompt
    })

    with st.chat_message("user"):
        st.markdown(action_prompt)

    # AI RESPONSE

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            qa_chain = get_qa_chain()

            response = qa_chain(action_prompt)

            answer = response["result"]

            st.markdown(answer)

            # SAVE AI MESSAGE
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

            # =========================
            # SOURCE CITATIONS
            # =========================

            st.markdown("---")
            st.markdown("## 📚 Source Citations")

            for doc in response["source_documents"]:

                source = doc.metadata.get("source", "Unknown")

                page = doc.metadata.get("page", "N/A")

                st.markdown(f"""
📄 **File:** {os.path.basename(source)}  
📑 **Page:** {page}
""")

                with st.expander("View Retrieved Chunk"):

                    st.write(doc.page_content[:1000])

else:
    if not st.session_state.vector_store_created:
        st.info("Upload documents to start chatting.")