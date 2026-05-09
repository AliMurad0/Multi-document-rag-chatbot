# 📚 Multi-Document RAG Chatbot

An AI-powered multi-document chatbot using Retrieval-Augmented Generation (RAG), semantic search, and LLMs.

Built with LangChain, FAISS, Groq LLMs, and Streamlit.

---

## 🚀 Features

- Multi-PDF upload
- DOCX and TXT support
- Conversational AI chat
- Semantic document search
- Source citations
- Retrieved chunk visualization
- PDF preview panel
- Chat history
- Key point generation
- Skill extraction
- Quiz generation
- Prompt-engineered grounded responses

---

## 🧠 Tech Stack

- Python
- Streamlit
- LangChain
- FAISS
- HuggingFace Embeddings
- Groq LLM
- Sentence Transformers

---

## 🏗 Architecture

User Query  
↓  
Retriever (FAISS)  
↓  
Relevant Chunks  
↓  
LLM (Groq Llama 3.1)  
↓  
Grounded AI Response

---

## ⚡ Installation

### Clone Repository

```bash
git clone https://github.com/your-username/rag-multi-doc-chatbot.git
cd rag-multi-doc-chatbot
```

### Create Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create `.env`

```env
GROQ_API_KEY=your_api_key_here
```

---

## ▶ Run Application

```bash
python -m streamlit run app.py
```

---

## 📸 Screenshots

(Add screenshots here)

---

## 📌 Future Improvements

- Authentication
- Streaming responses
- Hybrid search
- Docker deployment
- Cloud vector databases
- Multi-user chat

---

## 👨‍💻 Author

Ali Murad