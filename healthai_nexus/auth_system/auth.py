import sqlite3
import hashlib
from datetime import datetime

class AuthSystem:
    """Simple authentication system"""
    
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize users database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT,
                created_at TEXT NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register(self, username, password, email=""):
        """Register new user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO users (username, password, email, created_at)
                VALUES (?, ?, ?, ?)
            """, (username, self.hash_password(password), email, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            return True, "Registration successful!"
        except sqlite3.IntegrityError:
            conn.close()
            return False, "Username already exists"
    
    def login(self, username, password):
        """Authenticate user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username FROM users 
            WHERE username = ? AND password = ?
        """, (username, self.hash_password(password)))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return True, {"id": user[0], "username": user[1]}
        return False, None
