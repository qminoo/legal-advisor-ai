from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    
    API_URL_CHAT: str
    API_URL_CHAT_HISTORY: str
    API_URL_SESSIONS: str

    class Config:
        env_file = ".env"

settings = Settings() 

api_key = settings.OPENAI_API_KEY 