from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from models.embeddings import get_embedding_model

def build_vectorstore(documents, provider="openai"):
    """Turn raw text docs into a FAISS vectorstore with silent fallback to HuggingFace if OpenAI fails."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    # Extract the string content from each Document object
    texts = [doc.page_content for doc in documents]

    # Pass the list of strings to create_documents
    docs = splitter.create_documents(texts)

    try:
        embeddings = get_embedding_model(provider=provider)
    except Exception:
        embeddings = get_embedding_model(provider="huggingface")

    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore


def retrieve_relevant_chunks(query, vectorstore, k=3):
    """Get top-k relevant chunks for a query"""
    return vectorstore.similarity_search(query, k=k)
