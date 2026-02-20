from database import Database
from typing import Optional, List, Dict
import json

db = Database()

# Student Profile Operations
def create_student_profile(user_id: int, headline: str, college_name: str, 
                          branch: str, current_semester: str, skills: str) -> bool:
    """Create student profile"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO student_profiles (user_id, headline, college_name, branch, current_semester, skills)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, headline, college_name, branch, current_semester, skills))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def get_student_profile(user_id: int) -> Optional[Dict]:
    """Get student profile"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT headline, college_name, branch, current_semester, skills
            FROM student_profiles WHERE user_id = ?
        ''', (user_id,))
        profile = cursor.fetchone()
        conn.close()
        
        if profile:
            return {
                'headline': profile[0],
                'college_name': profile[1],
                'branch': profile[2],
                'current_semester': profile[3],
                'skills': profile[4]
            }
        return None
    except:
        return None

def update_student_profile(user_id: int, headline: str, college_name: str, 
                           branch: str, current_semester: str, skills: str) -> bool:
    """Update student profile"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE student_profiles 
            SET headline = ?, college_name = ?, branch = ?, current_semester = ?, skills = ?
            WHERE user_id = ?
        ''', (headline, college_name, branch, current_semester, skills, user_id))
        conn.commit()
        conn.close()
        return True
    except:
        return False

# Employee Profile Operations
def create_employee_profile(user_id: int, headline: str, company_name: str, 
                           job_title: str, industry: str, years_of_experience: int, skills: str) -> bool:
    """Create employee profile"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO employee_profiles (user_id, headline, company_name, job_title, industry, years_of_experience, skills)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, headline, company_name, job_title, industry, years_of_experience, skills))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def get_employee_profile(user_id: int) -> Optional[Dict]:
    """Get employee profile"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT headline, company_name, job_title, industry, years_of_experience, skills
            FROM employee_profiles WHERE user_id = ?
        ''', (user_id,))
        profile = cursor.fetchone()
        conn.close()
        
        if profile:
            return {
                'headline': profile[0],
                'company_name': profile[1],
                'job_title': profile[2],
                'industry': profile[3],
                'years_of_experience': profile[4],
                'skills': profile[5]
            }
        return None
    except:
        return None

def update_employee_profile(user_id: int, headline: str, company_name: str, 
                            job_title: str, industry: str, years_of_experience: int, skills: str) -> bool:
    """Update employee profile"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE employee_profiles 
            SET headline = ?, company_name = ?, job_title = ?, industry = ?, years_of_experience = ?, skills = ?
            WHERE user_id = ?
        ''', (headline, company_name, job_title, industry, years_of_experience, skills, user_id))
        conn.commit()
        conn.close()
        return True
    except:
        return False

# Company Profile Operations
def create_company_profile(user_id: int, location: str, description: str) -> bool:
    """Create company profile"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO company_profiles (user_id, location, description)
            VALUES (?, ?, ?)
        ''', (user_id, location, description))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def get_company_profile(user_id: int) -> Optional[Dict]:
    """Get company profile"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT location, description FROM company_profiles WHERE user_id = ?
        ''', (user_id,))
        profile = cursor.fetchone()
        conn.close()
        
        if profile:
            return {
                'location': profile[0],
                'description': profile[1]
            }
        return None
    except:
        return None

def update_company_profile(user_id: int, location: str, description: str) -> bool:
    """Update company profile"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE company_profiles SET location = ?, description = ? WHERE user_id = ?
        ''', (location, description, user_id))
        conn.commit()
        conn.close()
        return True
    except:
        return False

# Project Operations
def add_project(user_id: int, project_name: str, description: str, 
                technologies: str, project_link: str) -> bool:
    """Add a project"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO projects (user_id, project_name, description, technologies, project_link)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, project_name, description, technologies, project_link))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def get_projects(user_id: int) -> List[Dict]:
    """Get all projects for a user"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, project_name, description, technologies, project_link, created_at
            FROM projects WHERE user_id = ? ORDER BY created_at DESC
        ''', (user_id,))
        projects = cursor.fetchall()
        conn.close()
        
        return [{
            'id': p[0],
            'project_name': p[1],
            'description': p[2],
            'technologies': p[3],
            'project_link': p[4],
            'created_at': p[5]
        } for p in projects]
    except:
        return []

def delete_project(project_id: int) -> bool:
    """Delete a project"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
        conn.commit()
        conn.close()
        return True
    except:
        return False

# Internship Operations
def add_internship(user_id: int, company_name: str, duration: str, skills_used: str) -> bool:
    """Add an internship"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO internships (user_id, company_name, duration, skills_used)
            VALUES (?, ?, ?, ?)
        ''', (user_id, company_name, duration, skills_used))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def get_internships(user_id: int) -> List[Dict]:
    """Get all internships for a user"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, company_name, duration, skills_used, created_at
            FROM internships WHERE user_id = ? ORDER BY created_at DESC
        ''', (user_id,))
        internships = cursor.fetchall()
        conn.close()
        
        return [{
            'id': i[0],
            'company_name': i[1],
            'duration': i[2],
            'skills_used': i[3],
            'created_at': i[4]
        } for i in internships]
    except:
        return []

def delete_internship(internship_id: int) -> bool:
    """Delete an internship"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM internships WHERE id = ?', (internship_id,))
        conn.commit()
        conn.close()
        return True
    except:
        return False

# Previous Experience Operations
def add_previous_experience(user_id: int, company: str, role: str, duration: str) -> bool:
    """Add previous experience"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO previous_experience (user_id, company, role, duration)
            VALUES (?, ?, ?, ?)
        ''', (user_id, company, role, duration))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def get_previous_experience(user_id: int) -> List[Dict]:
    """Get all previous experience for a user"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, company, role, duration, created_at
            FROM previous_experience WHERE user_id = ? ORDER BY created_at DESC
        ''', (user_id,))
        experiences = cursor.fetchall()
        conn.close()
        
        return [{
            'id': e[0],
            'company': e[1],
            'role': e[2],
            'duration': e[3],
            'created_at': e[4]
        } for e in experiences]
    except:
        return []

def delete_previous_experience(experience_id: int) -> bool:
    """Delete previous experience"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM previous_experience WHERE id = ?', (experience_id,))
        conn.commit()
        conn.close()
        return True
    except:
        return False