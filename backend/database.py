"""
Database module for EduGenie
Handles user progress, topics, and history storage using SQLite
"""
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
from config import Config
import hashlib

class Database:
    """SQLite database handler for EduGenie"""
    
    def __init__(self, db_path: str = Config.DATABASE_PATH):
        """Initialize database connection and create tables if they don't exist"""
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return conn
    
    def init_database(self):
        """Create database tables if they don't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                learning_level TEXT DEFAULT 'Beginner',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Study sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS study_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                topic TEXT NOT NULL,
                learning_level TEXT NOT NULL,
                explanation TEXT,
                summary TEXT,
                quiz_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # User feedback table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                rating INTEGER,
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES study_sessions (id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_user(self, username: str, learning_level: str = "Beginner") -> int:
        """Create a new user or return existing user ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO users (username, learning_level) VALUES (?, ?)",
                (username, learning_level)
            )
            conn.commit()
            user_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            # User already exists, get their ID
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            user_id = cursor.fetchone()[0]
        
        conn.close()
        return user_id
    
    def save_session(
        self,
        user_id: int,
        topic: str,
        learning_level: str,
        explanation: str,
        summary: str,
        quiz_data: Dict
    ) -> int:
        """Save a study session to database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO study_sessions 
            (user_id, topic, learning_level, explanation, summary, quiz_data)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            topic,
            learning_level,
            explanation,
            summary,
            json.dumps(quiz_data)
        ))
        
        conn.commit()
        session_id = cursor.lastrowid
        conn.close()
        return session_id
    
    def get_user_history(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Get user's study history"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, topic, learning_level, created_at
            FROM study_sessions
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (user_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_session(self, session_id: int) -> Optional[Dict]:
        """Get a specific study session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM study_sessions WHERE id = ?
        """, (session_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            session = dict(row)
            session['quiz_data'] = json.loads(session['quiz_data'])
            return session
        return None
    
    def save_feedback(self, session_id: int, rating: int, comment: str = "") -> int:
        """Save user feedback for a session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO feedback (session_id, rating, comment)
            VALUES (?, ?, ?)
        """, (session_id, rating, comment))
        
        conn.commit()
        feedback_id = cursor.lastrowid
        conn.close()
        return feedback_id
    
    def get_user_stats(self, user_id: int) -> Dict:
        """Get user statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total_sessions,
                COUNT(DISTINCT topic) as unique_topics
            FROM study_sessions
            WHERE user_id = ?
        """, (user_id,))
        
        stats = dict(cursor.fetchone())
        conn.close()
        return stats

    # ------------------ AUTH SYSTEM ------------------

    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user_account(self, username: str, password: str, learning_level: str = "Beginner") -> bool:
        """Create a new account with password authentication"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            password_hash = self.hash_password(password)
            cursor.execute("""
                INSERT INTO users (username, learning_level) VALUES (?, ?)
            """, (username, learning_level))
            user_id = cursor.lastrowid
            cursor.execute("""
                ALTER TABLE users ADD COLUMN password_hash TEXT
            """)  # silently skip if already exists
        except sqlite3.OperationalError:
            pass  # password_hash column exists already

        try:
            cursor.execute("UPDATE users SET password_hash = ? WHERE username = ?", 
                           (self.hash_password(password), username))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False

    def authenticate_user(self, username: str, password: str) -> Optional[int]:
        """Check username-password match and return user_id"""
        conn = self.get_connection()
        cursor = conn.cursor()
        password_hash = self.hash_password(password)
        cursor.execute("SELECT id FROM users WHERE username = ? AND password_hash = ?", 
                       (username, password_hash))
        user = cursor.fetchone()
        conn.close()
        return user['id'] if user else None
