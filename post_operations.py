from database import Database
from typing import Optional, List, Dict
import json

db = Database()

def create_normal_post(user_id: int, content: str, file_data: bytes = None, 
                       file_type: str = None) -> tuple[bool, str]:
    """Create a normal post"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO posts (user_id, post_type, content, file_data, file_type, visibility)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, 'normal', content, file_data, file_type, 'public'))
        conn.commit()
        conn.close()
        return True, "Post created successfully"
    except Exception as e:
        return False, str(e)

def create_job_seeking_post(user_id: int, looking_for: str, role_domain: str, 
                            skills: str, preferred_location: str, description: str) -> tuple[bool, str]:
    """Create a job/internship seeking post"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO posts (user_id, post_type, looking_for, role_domain, required_skills, 
                             preferred_location, content, visibility)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, 'job_seeking', looking_for, role_domain, skills, preferred_location, 
              description, 'own'))
        conn.commit()
        conn.close()
        return True, "Job seeking post created successfully"
    except Exception as e:
        return False, str(e)

def create_company_job_post(user_id: int, job_title: str, required_skills: str, 
                           experience: str, job_type: str, job_location: str, 
                           job_description: str) -> tuple[bool, str]:
    """Create a company job post"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO posts (user_id, post_type, job_title, required_skills, experience, 
                             job_type, job_location, job_description, visibility)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, 'company_job', job_title, required_skills, experience, job_type, 
              job_location, job_description, 'public'))
        conn.commit()
        conn.close()
        return True, "Job post created successfully"
    except Exception as e:
        return False, str(e)

def get_user_normal_posts(user_id: int) -> List[Dict]:
    """Get user's own normal posts"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, content, file_data, file_type, created_at
            FROM posts WHERE user_id = ? AND post_type = 'normal' AND visibility = 'public'
            ORDER BY created_at DESC
        ''', (user_id,))
        posts = cursor.fetchall()
        conn.close()
        
        return [{
            'id': p[0],
            'user_id': user_id,
            'content': p[1],
            'file_data': p[2],
            'file_type': p[3],
            'created_at': p[4]
        } for p in posts]
    except:
        return []

def get_user_job_seeking_posts(user_id: int) -> List[Dict]:
    """Get user's job seeking posts"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, looking_for, role_domain, required_skills, preferred_location, content, created_at
            FROM posts WHERE user_id = ? AND post_type = 'job_seeking'
            ORDER BY created_at DESC
        ''', (user_id,))
        posts = cursor.fetchall()
        conn.close()
        
        return [{
            'id': p[0],
            'user_id': user_id,
            'looking_for': p[1],
            'role_domain': p[2],
            'required_skills': p[3],
            'preferred_location': p[4],
            'content': p[5],
            'created_at': p[6]
        } for p in posts]
    except:
        return []

def get_company_job_posts(user_id: int) -> List[Dict]:
    """Get company's own job posts"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, job_title, required_skills, experience, job_type, job_location, job_description, created_at
            FROM posts WHERE user_id = ? AND post_type = 'company_job'
            ORDER BY created_at DESC
        ''', (user_id,))
        posts = cursor.fetchall()
        conn.close()
        
        return [{
            'id': p[0],
            'user_id': user_id,
            'job_title': p[1],
            'required_skills': p[2],
            'experience': p[3],
            'job_type': p[4],
            'job_location': p[5],
            'job_description': p[6],
            'created_at': p[7]
        } for p in posts]
    except:
        return []

def get_all_job_seeking_posts(exclude_user_id: int = None) -> List[Dict]:
    """Get all job seeking posts (for companies to view)"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        if exclude_user_id:
            cursor.execute('''
                SELECT p.id, p.user_id, p.looking_for, p.role_domain, p.required_skills, 
                       p.preferred_location, p.content, p.created_at, u.full_name, u.profile_photo
                FROM posts p
                JOIN users u ON p.user_id = u.id
                WHERE p.post_type = 'job_seeking' AND p.user_id != ?
                ORDER BY p.created_at DESC
            ''', (exclude_user_id,))
        else:
            cursor.execute('''
                SELECT p.id, p.user_id, p.looking_for, p.role_domain, p.required_skills, 
                       p.preferred_location, p.content, p.created_at, u.full_name, u.profile_photo
                FROM posts p
                JOIN users u ON p.user_id = u.id
                WHERE p.post_type = 'job_seeking'
                ORDER BY p.created_at DESC
            ''')
        
        posts = cursor.fetchall()
        conn.close()
        
        return [{
            'id': p[0],
            'user_id': p[1],
            'looking_for': p[2],
            'role_domain': p[3],
            'required_skills': p[4],
            'preferred_location': p[5],
            'content': p[6],
            'created_at': p[7],
            'user_name': p[8],
            'user_photo': p[9]
        } for p in posts]
    except:
        return []

def get_all_company_job_posts(exclude_user_id: int = None) -> List[Dict]:
    """Get all company job posts"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        if exclude_user_id:
            cursor.execute('''
                SELECT p.id, p.user_id, p.job_title, p.required_skills, p.experience, 
                       p.job_type, p.job_location, p.job_description, p.created_at, 
                       u.full_name, u.profile_photo
                FROM posts p
                JOIN users u ON p.user_id = u.id
                WHERE p.post_type = 'company_job' AND p.user_id != ?
                ORDER BY p.created_at DESC
            ''', (exclude_user_id,))
        else:
            cursor.execute('''
                SELECT p.id, p.user_id, p.job_title, p.required_skills, p.experience, 
                       p.job_type, p.job_location, p.job_description, p.created_at, 
                       u.full_name, u.profile_photo
                FROM posts p
                JOIN users u ON p.user_id = u.id
                WHERE p.post_type = 'company_job'
                ORDER BY p.created_at DESC
            ''')
        
        posts = cursor.fetchall()
        conn.close()
        
        return [{
            'id': p[0],
            'user_id': p[1],
            'job_title': p[2],
            'required_skills': p[3],
            'experience': p[4],
            'job_type': p[5],
            'job_location': p[6],
            'job_description': p[7],
            'created_at': p[8],
            'company_name': p[9],
            'company_logo': p[10]
        } for p in posts]
    except:
        return []

def get_all_normal_posts(exclude_user_id: int = None) -> List[Dict]:
    """Get all normal posts from other users"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        if exclude_user_id:
            cursor.execute('''
                SELECT p.id, p.user_id, p.content, p.file_data, p.file_type, p.created_at,
                       u.full_name, u.profile_photo, u.profile_type
                FROM posts p
                JOIN users u ON p.user_id = u.id
                WHERE p.post_type = 'normal' AND p.user_id != ?
                ORDER BY p.created_at DESC
            ''', (exclude_user_id,))
        else:
            cursor.execute('''
                SELECT p.id, p.user_id, p.content, p.file_data, p.file_type, p.created_at,
                       u.full_name, u.profile_photo, u.profile_type
                FROM posts p
                JOIN users u ON p.user_id = u.id
                WHERE p.post_type = 'normal'
                ORDER BY p.created_at DESC
            ''')
        
        posts = cursor.fetchall()
        conn.close()
        
        return [{
            'id': p[0],
            'user_id': p[1],
            'content': p[2],
            'file_data': p[3],
            'file_type': p[4],
            'created_at': p[5],
            'user_name': p[6],
            'user_photo': p[7],
            'profile_type': p[8]
        } for p in posts]
    except:
        return []

def delete_post(post_id: int, user_id: int) -> bool:
    """Delete a post"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM posts WHERE id = ? AND user_id = ?', (post_id, user_id))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def get_post_by_id(post_id: int) -> Optional[Dict]:
    """Get post details by ID"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.*, u.full_name, u.profile_photo, u.profile_type
            FROM posts p
            JOIN users u ON p.user_id = u.id
            WHERE p.id = ?
        ''', (post_id,))
        post = cursor.fetchone()
        conn.close()
        
        if post:
            return {
                'id': post[0],
                'user_id': post[1],
                'post_type': post[2],
                'content': post[3],
                'file_data': post[4],
                'file_type': post[5],
                'user_name': post[-3],
                'user_photo': post[-2],
                'profile_type': post[-1]
            }
        return None
    except:
        return None