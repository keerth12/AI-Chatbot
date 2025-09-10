# 🤖 AI Chatbot with Streamlit

An interactive **AI-powered chatbot** built using **Streamlit** and **Groq**, designed to provide intelligent and context-aware responses. The chatbot supports **web search**, **document-based retrieval (RAG)**, **response customization**, and **chat history management**, making it a versatile assistant for day-to-day queries.

🌐 **Live Demo**: [Try it here](https://ai-chatbotgit-dnsemdrkcguxy6rpsfrhkf.streamlit.app/)

---

## 🚀 Features

* 🗨️ **Interactive Chat** – Engage in real-time conversation with the chatbot powered by **Groq**.
* 📚 **RAG (Retrieval-Augmented Generation)** – Upload local documents; chatbot retrieves relevant chunks using embeddings.
* 🌍 **Web Search Integration (Tavily API)** – Fetch up-to-date information from the internet.
* 📝 **Response Modes** – Switch between **Concise** and **Detailed** answers.
* 🔄 **Clear Chat History** – Start fresh conversations anytime.
* 🎨 **User-Friendly UI** – Clean Streamlit-based interface with navigation and customization options.

---

## ✅ Completed Tasks

1. **RAG Integration (Retrieval-Augmented Generation)**

   * Added ability for the chatbot to reference local documents/knowledge bases.
   * Implemented vector embeddings stored in `models/embeddings.py`.
   * Retrieval logic handled in `utils/`.
   * Chatbot responds contextually when relevant queries are asked from uploaded documents.

2. **Live Web Search Integration**

   * Integrated real-time web search when the LLM lacks knowledge.
   * Logic maintained in `utils/`, API keys stored in `config/`.

3. **Response Modes: Concise vs Detailed**

   * UI toggle implemented to allow users to choose between short replies or in-depth responses.

---

## 📷 Screenshot

![Page Overview](./Page%20overview.png)


---

## 🛠️ Installation & Setup

```bash
git clone https://github.com/your-username/AI-Chatbot.git
cd AI-Chatbot

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt
```

Add your API keys in a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Run the app:

```bash
streamlit run app.py
```

---

## 📖 Usage

* Type your query in the chat box.
* Select **Concise** or **Detailed** mode.
* Enable **Web Search** or **RAG Mode** depending on your needs.
* Upload documents for RAG-based responses.
* Clear chat history anytime for a fresh start.

---

## 📂 Project Structure

```
AI-Chatbot/
│── app.py                 # Main Streamlit app
│── requirements.txt       # Dependencies
│── config/                # API key & settings
│── models/embeddings.py   # Embedding models for RAG
│── utils/                 # Helper functions (RAG & Web Search logic)
│── README.md              # Project documentation
│── screenshot.png         # App screenshot
```

---

## 🙌 Credits

* Built with [Streamlit](https://streamlit.io/)
* AI responses powered by **Groq**
* Web search via **Tavily API**

---

## 📜 License

This project is licensed under the **MIT License**.

---

