import os
import requests

API_URL_CHAT = os.getenv("API_URL_CHAT", "http://localhost:8000/chat")

def send_chat_request(question):
    response = requests.post(
        API_URL_CHAT,
        json={"question": question},
        headers={"Content-Type": "application/json"}
    )
    return response
