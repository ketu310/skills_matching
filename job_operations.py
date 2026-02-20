from database import Database
from typing import List, Dict, Optional
import notification_operations as notif_ops

db = Database()

# Job Application Operations
def apply_for_job(user_id: int, post_id: int, company_id: int) -> tuple[bool, str]:
    """Apply for a job"""
    # Check if user already works in this company
    if is_employee(company_id, user_id):
        return False, "You are already in this company"
    
    # Check if already applied
    if has_applied(user_id, post_id):
        return False, "You have already applied for this job"
    
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO job_applications (user_id, post_id, company_id, status)
            VALUES (?, ?, ?, ?)
        ''', (user_id, post_id, company_id, 'pending'))
        conn.commit()
        conn.close()
        
        # Send notification to company
        user = db.get_user_by_id(user_id)
        company = db.get_user_by_id(company_id)
        notif_ops.create_notification(
            company_id,
            user_id,
            'job_application',
            f"{user['full_name']} applied for your job post",
            post_id
        )
        
        return True, "Application submitted successfully"
    except Exception as e:
        return False, str(e)

def has_applied(user_id: int, post_id: int) -> bool:
    """Check if user has already applied for a job"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id FROM job_applications 
            WHERE user_id = ? AND post_id = ?
        ''', (user_id, post_id))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except:
        return False

def get_user_applications(user_id: int) -> List[Dict]:
    """Get all job applications by a user"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT ja.id, ja.post_id, ja.company_id, ja.status, ja.created_at,
                   p.job_title, p.required_skills, p.experience, p.job_type, 
                   p.job_location, p.job_description,
                   u.full_name as company_name, u.profile_photo as company_logo
            FROM job_applications ja
            JOIN posts p ON ja.post_id = p.id
            JOIN users u ON ja.company_id = u.id
            WHERE ja.user_id = ?
            ORDER BY ja.created_at DESC
        ''', (user_id,))
        applications = cursor.fetchall()
        conn.close()
        
        return [{
            'id': a[0],
            'post_id': a[1],
            'company_id': a[2],
            'status': a[3],
            'created_at': a[4],
            'job_title': a[5],
            'required_skills': a[6],
            'experience': a[7],
            'job_type': a[8],
            'job_location': a[9],
            'job_description': a[10],
            'company_name': a[11],
            'company_logo': a[12]
        } for a in applications]
    except:
        return []

def accept_job_application(application_id: int) -> tuple[bool, str]:
    """Accept a job application and add user as employee"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Get application details
        cursor.execute('''
            SELECT user_id, company_id FROM job_applications WHERE id = ?
        ''', (application_id,))
        app = cursor.fetchone()
        
        if not app:
            conn.close()
            return False, "Application not found"
        
        user_id, company_id = app[0], app[1]
        
        # Update application status
        cursor.execute('''
            UPDATE job_applications SET status = 'accepted' WHERE id = ?
        ''', (application_id,))
        
        # Add to employees table
        try:
            cursor.execute('''
                INSERT INTO employees (company_id, user_id) VALUES (?, ?)
            ''', (company_id, user_id))
        except:
            pass  # Already exists
        
        conn.commit()
        conn.close()
        
        # Send notification to user
        company = db.get_user_by_id(company_id)
        notif_ops.create_notification(
            user_id,
            company_id,
            'application_accepted',
            f"{company['full_name']} accepted your job application"
        )
        
        return True, "Successfully accepted!"
    except Exception as e:
        return False, str(e)

# Company Approach Operations
def approach_candidate(company_id: int, user_id: int, post_id: int) -> tuple[bool, str]:
    """Company approaches a candidate"""
    # Check if user already works in this company
    if is_employee(company_id, user_id):
        return False, "This user already works in your company"
    
    # Check if already approached
    if has_approached(company_id, user_id, post_id):
        return False, "You have already approached this candidate"
    
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO company_approaches (company_id, user_id, post_id, status)
            VALUES (?, ?, ?, ?)
        ''', (company_id, user_id, post_id, 'pending'))
        conn.commit()
        conn.close()
        
        # Send notification to user
        company = db.get_user_by_id(company_id)
        notif_ops.create_notification(
            user_id,
            company_id,
            'company_approach',
            f"{company['full_name']} approached you for a position",
            post_id
        )
        
        return True, "Successfully approached!"
    except Exception as e:
        return False, str(e)

def has_approached(company_id: int, user_id: int, post_id: int) -> bool:
    """Check if company has already approached this candidate"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id FROM company_approaches 
            WHERE company_id = ? AND user_id = ? AND post_id = ?
        ''', (company_id, user_id, post_id))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except:
        return False

def get_company_approaches(user_id: int) -> List[Dict]:
    """Get all approaches received by a user"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT ca.id, ca.company_id, ca.post_id, ca.status, ca.created_at,
                   u.full_name as company_name, u.profile_photo as company_logo
            FROM company_approaches ca
            JOIN users u ON ca.company_id = u.id
            WHERE ca.user_id = ?
            ORDER BY ca.created_at DESC
        ''', (user_id,))
        approaches = cursor.fetchall()
        conn.close()
        
        return [{
            'id': a[0],
            'company_id': a[1],
            'post_id': a[2],
            'status': a[3],
            'created_at': a[4],
            'company_name': a[5],
            'company_logo': a[6]
        } for a in approaches]
    except:
        return []

def accept_company_approach(approach_id: int) -> tuple[bool, str]:
    """Accept a company approach and become employee"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Get approach details
        cursor.execute('''
            SELECT company_id, user_id FROM company_approaches WHERE id = ?
        ''', (approach_id,))
        app = cursor.fetchone()
        
        if not app:
            conn.close()
            return False, "Approach not found"
        
        company_id, user_id = app[0], app[1]
        
        # Update approach status
        cursor.execute('''
            UPDATE company_approaches SET status = 'accepted' WHERE id = ?
        ''', (approach_id,))
        
        # Add to employees table
        try:
            cursor.execute('''
                INSERT INTO employees (company_id, user_id) VALUES (?, ?)
            ''', (company_id, user_id))
        except:
            pass  # Already exists
        
        conn.commit()
        conn.close()
        
        # Send notification to company
        user = db.get_user_by_id(user_id)
        notif_ops.create_notification(
            company_id,
            user_id,
            'approach_accepted',
            f"{user['full_name']} accepted your approach"
        )
        
        return True, "Successfully accepted!"
    except Exception as e:
        return False, str(e)

# Employee Relationship Operations
def is_employee(company_id: int, user_id: int) -> bool:
    """Check if user is an employee of the company"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id FROM employees WHERE company_id = ? AND user_id = ?
        ''', (company_id, user_id))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except:
        return False

def get_company_employees(company_id: int) -> List[Dict]:
    """Get all employees of a company"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT e.id, e.user_id, e.created_at,
                   u.full_name, u.profile_photo, u.profile_type
            FROM employees e
            JOIN users u ON e.user_id = u.id
            WHERE e.company_id = ?
            ORDER BY e.created_at DESC
        ''', (company_id,))
        employees = cursor.fetchall()
        conn.close()
        
        return [{
            'id': e[0],
            'user_id': e[1],
            'joined_at': e[2],
            'full_name': e[3],
            'profile_photo': e[4],
            'profile_type': e[5]
        } for e in employees]
    except:
        return []

# Matching Operations
def calculate_match_score(user_skills: str, user_experience: int, 
                         job_skills: str, job_experience: str) -> Dict:
    """Calculate match score between user and job"""
    try:
        # Parse skills
        user_skills_list = [s.strip().lower() for s in user_skills.split(',') if s.strip()]
        job_skills_list = [s.strip().lower() for s in job_skills.split(',') if s.strip()]
        
        # Calculate skill match
        matched_skills = [s for s in user_skills_list if s in job_skills_list]
        missing_skills = [s for s in job_skills_list if s not in user_skills_list]
        
        skill_match_percentage = 0
        if job_skills_list:
            skill_match_percentage = (len(matched_skills) / len(job_skills_list)) * 100
        
        # Parse experience requirement
        try:
            required_exp = int(job_experience.split()[0]) if job_experience else 0
        except:
            required_exp = 0
        
        # Calculate experience match
        exp_match_percentage = 100
        if required_exp > 0:
            if user_experience >= required_exp:
                exp_match_percentage = 100
            else:
                exp_match_percentage = (user_experience / required_exp) * 100
        
        # Overall match (70% skills, 30% experience)
        overall_match = (skill_match_percentage * 0.7) + (exp_match_percentage * 0.3)
        
        return {
            'overall_match': round(overall_match, 2),
            'skill_match': round(skill_match_percentage, 2),
            'exp_match': round(exp_match_percentage, 2),
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'user_experience': user_experience,
            'required_experience': required_exp
        }
    except:
        return {
            'overall_match': 0,
            'skill_match': 0,
            'exp_match': 0,
            'matched_skills': [],
            'missing_skills': [],
            'user_experience': 0,
            'required_experience': 0
        }