import os
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

def get_chat_model():
    """
    Returns a chat model depending on which API key is set.
    Priority: Groq > OpenAI > Google Gemini.
    Returns None if no valid key is found.
    """
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key and groq_key.strip() != "":
        return ChatGroq(model="llama-3.1-8b-instant", api_key=groq_key)

    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and openai_key.strip() != "":
        return ChatOpenAI(model="gpt-4o-mini", api_key=openai_key)

    gemini_key = os.getenv("GOOGLE_API_KEY")
    if gemini_key and gemini_key.strip() != "":
        return ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=gemini_key)

    # Nothing found → return None (no ❌ error)
    return None



