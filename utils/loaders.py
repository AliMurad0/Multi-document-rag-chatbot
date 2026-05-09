from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader
)

import os


def load_documents(uploaded_files):

    documents = []

    os.makedirs("data", exist_ok=True)

    for file in uploaded_files:

        file_path = os.path.join("data", file.name)

        with open(file_path, "wb") as f:
            f.write(file.getbuffer())

        if file.name.endswith(".pdf"):
            loader = PyPDFLoader(file_path)

        elif file.name.endswith(".docx"):
            loader = Docx2txtLoader(file_path)

        elif file.name.endswith(".txt"):
            loader = TextLoader(file_path)

        else:
            continue

        documents.extend(loader.load())

    return documents