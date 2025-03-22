import os
import requests
from typing import Optional

API_URL_CHAT = os.getenv("API_URL_CHAT", "http://localhost:8000/chat")
API_URL_CHAT_HISTORY = os.getenv("API_URL_CHAT_HISTORY", "http://localhost:8000/chat-history")
API_URL_ALL_SESSIONS = os.getenv("API_URL_ALL_SESSIONS", "http://localhost:8000/all-sessions")

def chat(message: str, session_id: Optional[int] = None) -> dict:
    params = {}
    if session_id:
        params["session_id"] = session_id
    
    response = requests.post(API_URL_CHAT, params=params, json={"message": message})
    if response.status_code != 200:
        raise Exception(f"API request failed: {response.text}")
    
    return response.json()

def get_chat_history(session_id: int) -> dict:
    url = f"{API_URL_CHAT_HISTORY}/{session_id}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch chat history: {response.text}")
    
    return response.json()

def get_all_sessions() -> dict:
    response = requests.get(API_URL_ALL_SESSIONS)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch all sessions: {response.text}")
    
    return response.json()