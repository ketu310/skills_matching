import re

def validate_email(email: str) -> tuple[bool, str]:
    """Validate email address - only Gmail allowed"""
    email = email.strip().lower()
    
    if not email:
        return False, "Email is required"
    
    if " " in email:
        return False, "Email cannot contain spaces"
    
    regex = r'^[a-z0-9._%+-]+@gmail\.com$'
    if not re.match(regex, email):
        return False, "Only valid Gmail address allowed"
    
    if email.startswith('.') or email.endswith('.'):
        return False, "Invalid email format"
    
    return True, "Valid email"

def validate_password(password: str) -> tuple[bool, str]:
    """
    Validate password:
    - At least 8 characters
    - At least 1 lowercase letter
    - At least 1 uppercase letter
    - At least 1 digit
    - At least 1 special symbol
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least 1 lowercase letter"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least 1 uppercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least 1 digit"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least 1 special symbol (!@#$%^&*(),.?\":{}|<>)"
    
    return True, "Valid password"

def validate_full_name(name: str) -> tuple[bool, str]:
    """Validate full name"""
    name = name.strip()
    
    if not name:
        return False, "Name is required"
    
    if len(name) < 2:
        return False, "Name must be at least 2 characters"
    
    if not re.match(r'^[a-zA-Z\s]+$', name):
        return False, "Name can only contain letters and spaces"
    
    return True, "Valid name"