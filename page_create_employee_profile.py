import streamlit as st
from database import Database
import profile_operations as prof_ops
from PIL import Image

db = Database()

def show_create_employee_profile():
    """Employee profile creation page"""
    st.markdown('<style>.profile-title{color:#0077B5;font-size:32px;font-weight:bold;margin-bottom:30px;}.section-header{color:#0077B5;font-size:22px;font-weight:600;margin-top:30px;margin-bottom:15px;border-bottom:2px solid #0077B5;padding-bottom:10px;}</style>', unsafe_allow_html=True)
    
    st.markdown('<p class="profile-title">💼 Create Employee Profile</p>', unsafe_allow_html=True)
    
    if 'num_prev_exp' not in st.session_state:
        st.session_state.num_prev_exp = 0
    if 'num_projects_emp' not in st.session_state:
        st.session_state.num_projects_emp = 1
    
    with st.form("employee_profile_form"):
        st.markdown('<p class="section-header">📋 Basic Information</p>', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 3])
        
        with col1:
            profile_photo = st.file_uploader("Profile Photo", type=['png', 'jpg', 'jpeg'])
            if profile_photo:
                st.image(Image.open(profile_photo), width=150)
        
        with col2:
            full_name = st.text_input("Full Name*", value=st.session_state.user['full_name'])
            headline = st.text_input("Professional Headline*", placeholder="e.g., Senior Software Engineer | Full Stack Developer")
        
        st.markdown('<p class="section-header">💼 Current Job</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            company_name = st.text_input("Company Name*")
            job_title = st.text_input("Job Title*")
        with col2:
            industry = st.text_input("Industry*", placeholder="e.g., Information Technology")
            years_exp = st.number_input("Years of Experience*", min_value=0, max_value=50, value=0)
        
        st.markdown('<p class="section-header">📚 Previous Experience (Optional)</p>', unsafe_allow_html=True)
        prev_experiences = []
        for i in range(st.session_state.num_prev_exp):
            st.markdown(f"**Experience {i+1}**")
            col1, col2, col3 = st.columns(3)
            with col1:
                prev_company = st.text_input(f"Company", key=f"prev_comp_{i}")
            with col2:
                prev_role = st.text_input(f"Role", key=f"prev_role_{i}")
            with col3:
                prev_duration = st.text_input(f"Duration", key=f"prev_dur_{i}")
            prev_experiences.append({'company': prev_company, 'role': prev_role, 'duration': prev_duration})
        
        st.markdown('<p class="section-header">💡 Skills</p>', unsafe_allow_html=True)
        skills = st.text_area("Technical Skills*", placeholder="e.g., Python, AWS, Docker, Kubernetes")
        
        st.markdown('<p class="section-header">🚀 Projects</p>', unsafe_allow_html=True)
        projects = []
        for i in range(st.session_state.num_projects_emp):
            col1, col2 = st.columns(2)
            with col1:
                proj_name = st.text_input(f"Project Name", key=f"emp_proj_name_{i}")
                proj_tech = st.text_input(f"Technologies", key=f"emp_proj_tech_{i}")
            with col2:
                proj_desc = st.text_area(f"Description", key=f"emp_proj_desc_{i}")
                proj_link = st.text_input(f"Link", key=f"emp_proj_link_{i}")
            projects.append({'name': proj_name, 'description': proj_desc, 'technologies': proj_tech, 'link': proj_link})
        
        submit = st.form_submit_button("Create Profile", use_container_width=True)
        
        if submit:
            if not all([full_name, headline, company_name, job_title, industry, skills]):
                st.error("❌ Please fill all required fields")
                return
            
            if profile_photo:
                photo_bytes = profile_photo.getvalue()
                db.update_profile_photo(st.session_state.user['id'], photo_bytes)
                st.session_state.user['profile_photo'] = photo_bytes
            
            success = prof_ops.create_employee_profile(
                st.session_state.user['id'], headline, company_name, 
                job_title, industry, years_exp, skills
            )
            
            if success:
                for proj in projects:
                    if proj['name']:
                        prof_ops.add_project(st.session_state.user['id'], proj['name'], 
                                           proj['description'], proj['technologies'], proj['link'])
                
                for exp in prev_experiences:
                    if exp['company']:
                        prof_ops.add_previous_experience(st.session_state.user['id'], 
                                                        exp['company'], exp['role'], exp['duration'])
                
                st.success("✅ Profile created successfully!")
                st.session_state.profile_created = True
                st.rerun()
    
    if st.session_state.get('profile_created', False):
        if st.button("Continue to Home", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
    else:
        if st.button("➕ Add Previous Experience"):
            st.session_state.num_prev_exp += 1
            st.rerun()
        if st.button("➕ Add Project"):
            st.session_state.num_projects_emp += 1
            st.rerun()