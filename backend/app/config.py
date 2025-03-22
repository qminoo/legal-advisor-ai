from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    OPENAI_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings() 

api_key = settings.OPENAI_API_KEY 