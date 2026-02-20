
import streamlit as st
from database import Database
import profile_operations as prof_ops
from PIL import Image
from io import BytesIO

db = Database()

def show_edit_profile():
    """Edit user's own profile with modern design"""
    
    # Modern styling
    st.markdown("""
        <style>
        /* Main background */
        .main {
            background: #f5f7fa;
        }
        
        /* Section card */
        .section-card {
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border-left: 4px solid #0077B5;
        }
        
        /* Item card for projects, internships, etc */
        .item-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
            border: 1px solid #e9ecef;
            transition: all 0.2s ease;
        }
        
        .item-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border-color: #0077B5;
        }
        
        /* Section headers */
        .section-header {
            color: #2c3e50;
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #0077B5;
        }
        
        /* Buttons */
        .stButton > button {
            background: #0077B5;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        
        .stButton > button:hover {
            background: #005582;
            transform: translateY(-1px);
        }
        
        /* Form labels */
        .stTextInput label, .stTextArea label, .stNumberInput label {
            font-weight: 600;
            color: #2c3e50;
        }
        </style>
    """, unsafe_allow_html=True)
    
    if st.button("⬅ Back to Home"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown("# ✏️ Edit Profile")
    
    user = st.session_state.user
    profile_type = user['profile_type']
    
    if profile_type == 'student':
        edit_student_profile()
    elif profile_type == 'employee':
        edit_employee_profile()
    elif profile_type == 'company':
        edit_company_profile()

def edit_student_profile():
    """Edit student profile with projects and internships"""
    profile = prof_ops.get_student_profile(st.session_state.user['id'])
    
    # Basic Information Section
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-header">📋 Basic Information</p>', unsafe_allow_html=True)
    
    with st.form("edit_student_basic"):
        profile_photo = st.file_uploader("Update Profile Photo", type=['png', 'jpg', 'jpeg'])
        
        col1, col2 = st.columns(2)
        with col1:
            headline = st.text_input("Headline/Bio", value=profile.get('headline', '') if profile else '', 
                                    placeholder="e.g., Computer Science Student | Python Developer")
            college = st.text_input("College/University", value=profile.get('college_name', '') if profile else '',
                                   placeholder="e.g., MIT")
            branch = st.text_input("Branch/Major", value=profile.get('branch', '') if profile else '',
                                  placeholder="e.g., Computer Science")
        
        with col2:
            semester = st.text_input("Current Semester/Year", value=profile.get('current_semester', '') if profile else '',
                                    placeholder="e.g., 6th Semester")
            skills = st.text_area("Skills (comma-separated)", value=profile.get('skills', '') if profile else '',
                                 placeholder="e.g., Python, Java, React, Machine Learning", height=100)
        
        if st.form_submit_button("💾 Save Basic Info", use_container_width=True):
            if profile_photo:
                photo_bytes = profile_photo.getvalue()
                db.update_profile_photo(st.session_state.user['id'], photo_bytes)
                st.session_state.user['profile_photo'] = photo_bytes
            
            prof_ops.update_student_profile(st.session_state.user['id'], headline, college, branch, semester, skills)
            st.success("✅ Profile updated successfully!")
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Projects Section
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-header">🚀 Projects</p>', unsafe_allow_html=True)
    
    projects = prof_ops.get_projects(st.session_state.user['id'])
    
    if projects:
        for proj in projects:
            st.markdown('<div class="item-card">', unsafe_allow_html=True)
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"### {proj['project_name']}")
                st.markdown(f"**Description:** {proj['description']}")
                st.markdown(f"**Technologies:** {proj['technologies']}")
                if proj['project_link']:
                    st.markdown(f"🔗 [View Project]({proj['project_link']})")
            with col2:
                if st.button("🗑️", key=f"del_proj_{proj['id']}", help="Delete Project"):
                    prof_ops.delete_project(proj['id'])
                    st.success("✅ Project deleted!")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("💡 No projects added yet. Add your first project below!")
    
    st.markdown("### ➕ Add New Project")
    with st.form("add_project_student"):
        proj_name = st.text_input("Project Name*", placeholder="e.g., E-commerce Website")
        proj_desc = st.text_area("Description*", placeholder="Describe what your project does...", height=100)
        proj_tech = st.text_input("Technologies Used* (comma-separated)", placeholder="e.g., React, Node.js, MongoDB")
        proj_link = st.text_input("Project Link/GitHub URL", placeholder="https://github.com/username/project")
        
        if st.form_submit_button("➕ Add Project", use_container_width=True):
            if proj_name and proj_desc and proj_tech:
                prof_ops.add_project(st.session_state.user['id'], proj_name, proj_desc, proj_tech, proj_link)
                st.success("✅ Project added successfully!")
                st.rerun()
            else:
                st.error("❌ Please fill in all required fields (marked with *)")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Internships Section
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-header">💼 Internships</p>', unsafe_allow_html=True)
    
    internships = prof_ops.get_internships(st.session_state.user['id'])
    
    if internships:
        for intern in internships:
            st.markdown('<div class="item-card">', unsafe_allow_html=True)
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"### {intern['company_name']}")
                st.markdown(f"**Duration:** {intern['duration']}")
                st.markdown(f"**Skills Used:** {intern['skills_used']}")
            with col2:
                if st.button("🗑️", key=f"del_intern_{intern['id']}", help="Delete Internship"):
                    prof_ops.delete_internship(intern['id'])
                    st.success("✅ Internship deleted!")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("💡 No internships added yet. Add your first internship below!")
    
    st.markdown("### ➕ Add New Internship")
    with st.form("add_internship_student"):
        int_company = st.text_input("Company Name*", placeholder="e.g., Google")
        int_duration = st.text_input("Duration*", placeholder="e.g., May 2024 - Aug 2024 (3 months)")
        int_skills = st.text_input("Skills Used* (comma-separated)", placeholder="e.g., Python, Django, AWS")
        
        if st.form_submit_button("➕ Add Internship", use_container_width=True):
            if int_company and int_duration and int_skills:
                prof_ops.add_internship(st.session_state.user['id'], int_company, int_duration, int_skills)
                st.success("✅ Internship added successfully!")
                st.rerun()
            else:
                st.error("❌ Please fill in all required fields (marked with *)")
    
    st.markdown('</div>', unsafe_allow_html=True)

def edit_employee_profile():
    """Edit employee profile with work experience"""
    profile = prof_ops.get_employee_profile(st.session_state.user['id'])
    
    # Basic Information Section
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-header">📋 Basic Information</p>', unsafe_allow_html=True)
    
    with st.form("edit_employee_basic"):
        profile_photo = st.file_uploader("Update Profile Photo", type=['png', 'jpg', 'jpeg'])
        
        col1, col2 = st.columns(2)
        with col1:
            headline = st.text_input("Professional Headline", value=profile.get('headline', '') if profile else '',
                                    placeholder="e.g., Senior Software Engineer | AI Specialist")
            company = st.text_input("Current Company", value=profile.get('company_name', '') if profile else '',
                                   placeholder="e.g., Google")
            job_title = st.text_input("Current Job Title", value=profile.get('job_title', '') if profile else '',
                                     placeholder="e.g., Senior Software Engineer")
        
        with col2:
            industry = st.text_input("Industry", value=profile.get('industry', '') if profile else '',
                                    placeholder="e.g., Technology, Finance, Healthcare")
            exp = st.number_input("Total Years of Experience", min_value=0, max_value=50, 
                                 value=profile.get('years_of_experience', 0) if profile else 0)
            skills = st.text_area("Skills (comma-separated)", value=profile.get('skills', '') if profile else '',
                                 placeholder="e.g., Python, Java, AWS, Leadership", height=100)
        
        if st.form_submit_button("💾 Save Basic Info", use_container_width=True):
            if profile_photo:
                photo_bytes = profile_photo.getvalue()
                db.update_profile_photo(st.session_state.user['id'], photo_bytes)
                st.session_state.user['profile_photo'] = photo_bytes
            
            prof_ops.update_employee_profile(st.session_state.user['id'], headline, company, 
                                            job_title, industry, exp, skills)
            st.success("✅ Profile updated successfully!")
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Work Experience Section
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-header">💼 Work Experience</p>', unsafe_allow_html=True)
    
    experiences = prof_ops.get_previous_experience(st.session_state.user['id'])
    
    if experiences:
        for exp in experiences:
            st.markdown('<div class="item-card">', unsafe_allow_html=True)
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"### {exp['role']}")
                st.markdown(f"**Company:** {exp['company']}")
                st.markdown(f"**Duration:** {exp['duration']}")
            with col2:
                if st.button("🗑️", key=f"del_exp_{exp['id']}", help="Delete Experience"):
                    prof_ops.delete_previous_experience(exp['id'])
                    st.success("✅ Experience deleted!")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("💡 No previous work experience added yet. Add your work history below!")
    
    st.markdown("### ➕ Add Work Experience")
    with st.form("add_experience_employee"):
        prev_company = st.text_input("Company Name*", placeholder="e.g., Microsoft")
        prev_role = st.text_input("Role/Position*", placeholder="e.g., Software Developer")
        prev_duration = st.text_input("Duration*", placeholder="e.g., Jan 2020 - Dec 2022")
        
        if st.form_submit_button("➕ Add Experience", use_container_width=True):
            if prev_company and prev_role and prev_duration:
                prof_ops.add_previous_experience(st.session_state.user['id'], 
                                                prev_company, prev_role, prev_duration)
                st.success("✅ Work experience added successfully!")
                st.rerun()
            else:
                st.error("❌ Please fill in all required fields (marked with *)")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Projects Section (Optional for employees)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-header">🚀 Projects (Optional)</p>', unsafe_allow_html=True)
    
    projects = prof_ops.get_projects(st.session_state.user['id'])
    
    if projects:
        for proj in projects:
            st.markdown('<div class="item-card">', unsafe_allow_html=True)
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"### {proj['project_name']}")
                st.markdown(f"**Description:** {proj['description']}")
                st.markdown(f"**Technologies:** {proj['technologies']}")
                if proj['project_link']:
                    st.markdown(f"🔗 [View Project]({proj['project_link']})")
            with col2:
                if st.button("🗑️", key=f"del_proj_{proj['id']}", help="Delete Project"):
                    prof_ops.delete_project(proj['id'])
                    st.success("✅ Project deleted!")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### ➕ Add New Project")
    with st.form("add_project_employee"):
        proj_name = st.text_input("Project Name", placeholder="e.g., Cloud Migration Platform")
        proj_desc = st.text_area("Description", placeholder="Describe your project...", height=100)
        proj_tech = st.text_input("Technologies Used (comma-separated)", placeholder="e.g., AWS, Docker, Kubernetes")
        proj_link = st.text_input("Project Link", placeholder="https://...")
        
        if st.form_submit_button("➕ Add Project", use_container_width=True):
            if proj_name and proj_desc and proj_tech:
                prof_ops.add_project(st.session_state.user['id'], proj_name, proj_desc, proj_tech, proj_link)
                st.success("✅ Project added successfully!")
                st.rerun()
            else:
                st.error("❌ Please fill in project name, description, and technologies")
    
    st.markdown('</div>', unsafe_allow_html=True)

def edit_company_profile():
    """Edit company profile"""
    profile = prof_ops.get_company_profile(st.session_state.user['id'])
    
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-header">🏢 Company Information</p>', unsafe_allow_html=True)
    
    with st.form("edit_company"):
        logo = st.file_uploader("Update Company Logo", type=['png', 'jpg', 'jpeg'])
        location = st.text_input("Location", value=profile.get('location', '') if profile else '',
                                placeholder="e.g., San Francisco, CA")
        description = st.text_area("Company Description", value=profile.get('description', '') if profile else '',
                                   placeholder="Describe your company, what you do, your mission...",
                                   height=200)
        
        if st.form_submit_button("💾 Save Changes", use_container_width=True):
            if logo:
                logo_bytes = logo.getvalue()
                db.update_profile_photo(st.session_state.user['id'], logo_bytes)
                st.session_state.user['profile_photo'] = logo_bytes
            
            prof_ops.update_company_profile(st.session_state.user['id'], location, description)
            st.success("✅ Company profile updated successfully!")
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    show_edit_profile()