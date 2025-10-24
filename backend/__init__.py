"""
EduGenie Backend Package
Contains AI engine, content processor, and database modules
"""
from .ai_engine import AIEngine
from .content_processor import ContentProcessor
from .database import Database

__all__ = ['AIEngine', 'ContentProcessor', 'Database']