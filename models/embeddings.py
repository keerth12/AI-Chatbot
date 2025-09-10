import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

def get_embedding_model(provider="openai"):
    """
    Returns an embedding model.
    provider: "openai" or "huggingface"
    """
    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        # Ensure that an API key is provided for OpenAI
        if not api_key or api_key.strip() == "":
            raise ValueError("OpenAI provider selected, but no API key found. Please set OPENAI_API_KEY environment variable.")
        return OpenAIEmbeddings(model="text-embedding-3-small", api_key=api_key)

    elif provider == "huggingface":
        # Using HuggingFace, which does not require an API key
        return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    else:
        raise ValueError("Unsupported provider. Choose 'openai' or 'huggingface'.")
