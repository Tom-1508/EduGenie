"""
Configuration file for EduGenie
Manages API keys and application settings
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration"""
    
    # Gemini API Key - Get from https://aistudio.google.com/app/apikey
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # Database settings
    DATABASE_PATH = "edugenie.db"
    
    # Learning levels
    LEARNING_LEVELS = ["Beginner", "Intermediate", "Advanced"]
    
    # File upload settings
    MAX_FILE_SIZE_MB = 10
    ALLOWED_EXTENSIONS = [".pdf", ".txt", ".docx"]
    
    # AI Model settings - Using LearnLM for education!
    GEMINI_MODEL = "learnlm-2.0-flash-experimental"  # Best for educational content!
    # Alternatives:
    # "gemini-2.5-flash" - Latest general model (fast & stable)
    # "gemini-2.5-pro" - Most powerful (slower but better quality)
    # "gemini-flash-latest" - Always uses newest flash model
    
    # Quiz settings
    DEFAULT_QUIZ_QUESTIONS = 5
    
    @staticmethod
    def validate():
        """Validate that required configuration is present"""
        if not Config.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY not found. Please set it in .env file or environment variables"
            )
        return True