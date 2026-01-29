# backend/core/config.py
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings:
    PROJECT_NAME: str = "HRMS Chatbot MVP"
    VERSION: str = "1.0.0"
    
    # API Keys
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    
    # Database
    DATABASE_URL: str = "sqlite:///./hrms_mvp.db"
    
    # Hashing Secret (Optional for stronger hashing)
    HASH_SALT: str = os.getenv("HASH_SALT", "mvp_secret_salt")

settings = Settings()