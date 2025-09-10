import streamlit as st
import os
import sys
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_community.document_loaders import TextLoader

# Add root project path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from models.llm import get_chat_model
from utils.rag_utils import build_vectorstore, retrieve_relevant_chunks
from utils.search_utils import search_web

# Use an absolute path to ensure the file is found regardless of the CWD
RAG_SOURCE_PATH = os.path.join(os.path.dirname(__file__), 'data', 'rag_source.txt')


# Initialize the vector store only once
@st.cache_resource
def get_vectorstore():
    """Build and return a vector store from local documents."""

    # Removed the explicit check for OPENAI_API_KEY
    # The application will now proceed to use other available providers.

    # Check RAG source file
    if not os.path.exists(RAG_SOURCE_PATH):
        st.error("📂 RAG source file not found. Please create a 'data' folder and add 'rag_source.txt'.")
        return None

    # Load docs and build vectorstore
    loader = TextLoader(RAG_SOURCE_PATH)
    documents = loader.load()
    try:
        # Use Hugging Face for embeddings, which is a free provider.
        vectorstore = build_vectorstore(documents, provider="huggingface")
        return vectorstore
    except Exception as e:
        st.error(f"⚠️ Failed to build vectorstore: {str(e)}")
        return None


def get_chat_response(chat_model, messages, system_prompt, rag_context=None):
    """Get response from the chat model with optional RAG context."""
    try:
        if rag_context:
            system_prompt = f"{system_prompt}\n\nRelevant Context: {rag_context}"

        formatted_messages = [SystemMessage(content=system_prompt)]

        for msg in messages:
            if msg["role"] == "user":
                formatted_messages.append(HumanMessage(content=msg["content"]))
            else:
                formatted_messages.append(AIMessage(content=msg["content"]))

        response = chat_model.invoke(formatted_messages)
        return response.content

    except Exception as e:
        return f"Error getting response: {str(e)}"


# def instructions_page():
#     """Instructions and setup page"""
#     st.title("The Chatbot Blueprint")
#     st.markdown("Welcome! Follow these instructions to set up and use the chatbot.")

#     st.markdown("""
#     ## 🛠️ Installation
#     ```bash
#     pip install -r requirements.txt
#     ```

#     ## 🔑 API Key Setup
#     You'll need API keys from your chosen provider. Set them as environment variables:
#     - **OpenAI** → `OPENAI_API_KEY`
#     - **Groq** → `GROQ_API_KEY`
#     - **Google Gemini** → `GOOGLE_API_KEY`

#     ## ⚙️ Models
#     - OpenAI → gpt-4o, gpt-4o-mini, gpt-3.5-turbo
#     - Groq → llama-3.1-70b-versatile, llama-3.1-8b-instant
#     - Gemini → gemini-1.5-pro, gemini-1.5-flash

#     ## 🚀 How to Use
#     1. Go to the **Chat** page.
#     2. Start chatting!

#     ## ❗ Troubleshooting
#     - API Key missing → Set environment variable
#     - Model not found → Check provider docs
#     - No internet → Verify connection
#     """)


def chat_page():
    """Main chat interface page"""
    vectorstore = get_vectorstore()

    with st.sidebar:
        response_mode = st.radio("Response Mode", ["Concise", "Detailed"], index=0)
        use_rag = st.checkbox("Use RAG (from local docs)", value=True)
        use_web_search = st.checkbox("Use Web Search (via Tavily)", value=False)

    mode_prompt = "Answer concisely." if response_mode == "Concise" else "Provide a detailed explanation."
    system_prompt = mode_prompt

    st.title("🤖 AI ChatBot")

    chat_model = get_chat_model()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if chat_model:
        if prompt := st.chat_input("Type your message here..."):
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Getting response..."):
                    rag_context = None
                    if use_rag and vectorstore:
                        chunks = retrieve_relevant_chunks(prompt, vectorstore)
                        rag_context = "\n".join([c.page_content for c in chunks])

                    if use_web_search:
                        web_results = search_web(prompt)
                        if rag_context:
                            rag_context += f"\n\nWeb Search Results:\n{web_results}"
                        else:
                            rag_context = f"Web Search Results:\n{web_results}"

                    response = get_chat_response(chat_model, st.session_state.messages, system_prompt, rag_context)
                    st.markdown(response)

            st.session_state.messages.append({"role": "assistant", "content": response})
    else:
        st.info("⚠️ No API keys found in environment variables. Please check the Instructions page to set up your API keys.")


def main():
    st.set_page_config(
        page_title="LangChain Multi-Provider ChatBot",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    with st.sidebar:
        st.title("Navigation")
        page = st.radio("Go to:", ["Chat"], index=0) #, "Instructions"

        if page == "Chat":
            st.divider()
            if st.button("🔄 Clear Chat History", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

    # if page == "Instructions":
    #     instructions_page()
    if page == "Chat":
        chat_page()


if __name__ == "__main__":
    main()