import requests
from config.config import TAVILY_API_KEY

def search_web(query):
    """
    Perform a web search using Tavily API.
    Docs: https://docs.tavily.com/
    """
    if not TAVILY_API_KEY:
        raise ValueError("⚠️ Please set TAVILY_API_KEY in environment variables")

    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "num_results": 3
    }

    resp = requests.post(url, json=payload, headers=headers)
    data = resp.json()
    results = [r["content"] for r in data.get("results", [])]
    return "\n".join(results)
