import sqlite3
import hashlib
from datetime import datetime
from typing import Optional, List, Dict, Any
import json

class Database:
    def __init__(self, db_name: str = "linkedin_mini.db"):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        """Create a database connection"""
        return sqlite3.connect(self.db_name, check_same_thread=False)
    
    def init_database(self):
        """Initialize all database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                profile_type TEXT NOT NULL,
                profile_photo BLOB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Student profiles
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS student_profiles (
                user_id INTEGER PRIMARY KEY,
                headline TEXT,
                college_name TEXT,
                branch TEXT,
                current_semester TEXT,
                skills TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Employee profiles
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employee_profiles (
                user_id INTEGER PRIMARY KEY,
                headline TEXT,
                company_name TEXT,
                job_title TEXT,
                industry TEXT,
                years_of_experience INTEGER,
                skills TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Company profiles
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS company_profiles (
                user_id INTEGER PRIMARY KEY,
                location TEXT,
                description TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Projects
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                project_name TEXT,
                description TEXT,
                technologies TEXT,
                project_link TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Internships
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS internships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                company_name TEXT,
                duration TEXT,
                skills_used TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Previous Experience
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS previous_experience (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                company TEXT,
                role TEXT,
                duration TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Posts
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                post_type TEXT,
                content TEXT,
                file_data BLOB,
                file_type TEXT,
                looking_for TEXT,
                role_domain TEXT,
                preferred_location TEXT,
                job_title TEXT,
                required_skills TEXT,
                experience TEXT,
                job_type TEXT,
                job_location TEXT,
                job_description TEXT,
                visibility TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Likes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS likes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER,
                user_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (post_id) REFERENCES posts(id),
                FOREIGN KEY (user_id) REFERENCES users(id),
                UNIQUE(post_id, user_id)
            )
        ''')
        
        # Comments
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER,
                user_id INTEGER,
                comment_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (post_id) REFERENCES posts(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Followers
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS followers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                follower_id INTEGER,
                following_id INTEGER,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (follower_id) REFERENCES users(id),
                FOREIGN KEY (following_id) REFERENCES users(id),
                UNIQUE(follower_id, following_id)
            )
        ''')
        
        # Job Applications
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                post_id INTEGER,
                company_id INTEGER,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (post_id) REFERENCES posts(id),
                FOREIGN KEY (company_id) REFERENCES users(id)
            )
        ''')
        
        # Company Approaches
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS company_approaches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER,
                user_id INTEGER,
                post_id INTEGER,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES users(id),
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (post_id) REFERENCES posts(id)
            )
        ''')
        
        # Employees (accepted relationships)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER,
                user_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES users(id),
                FOREIGN KEY (user_id) REFERENCES users(id),
                UNIQUE(company_id, user_id)
            )
        ''')
        
        # Notifications
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                from_user_id INTEGER,
                notification_type TEXT,
                message TEXT,
                post_id INTEGER,
                is_read INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (from_user_id) REFERENCES users(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_user(self, full_name: str, email: str, password: str) -> tuple[bool, str]:
        """Create a new user — stores password as plain text"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                'INSERT INTO users (full_name, email, password, profile_type) VALUES (?, ?, ?, ?)',
                (full_name, email, password, 'pending')
            )
            conn.commit()
            conn.close()
            return True, "User created successfully"
        except sqlite3.IntegrityError:
            return False, "Email already exists"
        except Exception as e:
            return False, str(e)
    
    def verify_user(self, email: str, password: str) -> tuple[bool, Optional[Dict]]:
        """Verify user credentials using plain text password"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                'SELECT id, full_name, email, profile_type, profile_photo FROM users WHERE email = ? AND password = ?',
                (email, password)
            )
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return True, {
                    'id': user[0],
                    'full_name': user[1],
                    'email': user[2],
                    'profile_type': user[3],
                    'profile_photo': user[4]
                }
            return False, None
        except Exception as e:
            return False, None
    
    def update_profile_type(self, user_id: int, profile_type: str) -> bool:
        """Update user's profile type"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET profile_type = ? WHERE id = ?', (profile_type, user_id))
            conn.commit()
            conn.close()
            return True
        except:
            return False
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT id, full_name, email, profile_type, profile_photo FROM users WHERE id = ?', (user_id,))
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return {
                    'id': user[0],
                    'full_name': user[1],
                    'email': user[2],
                    'profile_type': user[3],
                    'profile_photo': user[4]
                }
            return None
        except:
            return None
    
    def update_profile_photo(self, user_id: int, photo_data: bytes) -> bool:
        """Update user's profile photo"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET profile_photo = ? WHERE id = ?', (photo_data, user_id))
            conn.commit()
            conn.close()
            return True
        except:
            return False
    
    def email_exists(self, email: str) -> bool:
        """Check if email exists"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
            result = cursor.fetchone()
            conn.close()
            return result is not None
        except:
            return False
    
    def get_all_users(self, exclude_user_id: int = None) -> List[Dict]:
        """Get all users except the specified one"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if exclude_user_id:
                cursor.execute(
                    'SELECT id, full_name, email, profile_type, profile_photo FROM users WHERE id != ? ORDER BY created_at DESC',
                    (exclude_user_id,)
                )
            else:
                cursor.execute('SELECT id, full_name, email, profile_type, profile_photo FROM users ORDER BY created_at DESC')
            
            users = cursor.fetchall()
            conn.close()
            
            return [{
                'id': user[0],
                'full_name': user[1],
                'email': user[2],
                'profile_type': user[3],
                'profile_photo': user[4]
            } for user in users]
        except:
            return []
    
    def search_users(self, query: str) -> List[Dict]:
        """Search users by name"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                'SELECT id, full_name, email, profile_type, profile_photo FROM users WHERE full_name LIKE ? ORDER BY full_name',
                (f'%{query}%',)
            )
            users = cursor.fetchall()
            conn.close()
            
            return [{
                'id': user[0],
                'full_name': user[1],
                'email': user[2],
                'profile_type': user[3],
                'profile_photo': user[4]
            } for user in users]
        except:
            return []