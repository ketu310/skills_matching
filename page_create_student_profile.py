import streamlit as st
from database import Database
import profile_operations as prof_ops
import io
from PIL import Image

db = Database()

def show_create_student_profile():
    """Student profile creation page"""
    st.markdown("""
        <style>
        .profile-title {
            color: #0077B5;
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 30px;
        }
        .section-header {
            color: #0077B5;
            font-size: 22px;
            font-weight: 600;
            margin-top: 30px;
            margin-bottom: 15px;
            border-bottom: 2px solid #0077B5;
            padding-bottom: 10px;
        }
        .stButton > button {
            background-color: #0077B5;
            color: white;
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="profile-title">📚 Create Student Profile</p>', unsafe_allow_html=True)
    
    # Initialize project and internship counters
    if 'num_projects' not in st.session_state:
        st.session_state.num_projects = 1
    if 'num_internships' not in st.session_state:
        st.session_state.num_internships = 0
    
    with st.form("student_profile_form"):
        # Basic Section
        st.markdown('<p class="section-header">📋 Basic Information</p>', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 3])
        
        with col1:
            profile_photo = st.file_uploader("Profile Photo", type=['png', 'jpg', 'jpeg'])
            if profile_photo:
                image = Image.open(profile_photo)
                st.image(image, width=150)
        
        with col2:
            full_name = st.text_input("Full Name*", value=st.session_state.user['full_name'])
            headline = st.text_input("Headline*", placeholder="e.g., Computer Science Student | Python Developer")
        
        # Education Section
        st.markdown('<p class="section-header">🎓 Education</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            college_name = st.text_input("College Name*")
            branch = st.text_input("Branch*", placeholder="e.g., Computer Science")
        with col2:
            current_semester = st.text_input("Current Semester/Year*", placeholder="e.g., 6th Semester")
        
        # Skills Section
        st.markdown('<p class="section-header">💡 Skills</p>', unsafe_allow_html=True)
        skills = st.text_area("Technical Skills* (comma-separated)", 
                             placeholder="e.g., Python, Java, Machine Learning, SQL, React")
        
        # Projects Section
        st.markdown('<p class="section-header">🚀 Projects</p>', unsafe_allow_html=True)
        projects = []
        for i in range(st.session_state.num_projects):
            st.markdown(f"**Project {i+1}**")
            col1, col2 = st.columns(2)
            with col1:
                proj_name = st.text_input(f"Project Name", key=f"proj_name_{i}")
                proj_tech = st.text_input(f"Technologies Used", key=f"proj_tech_{i}",
                                         placeholder="e.g., Python, Flask, MySQL")
            with col2:
                proj_desc = st.text_area(f"Description", key=f"proj_desc_{i}",
                                        placeholder="Brief description of the project")
                proj_link = st.text_input(f"Project Link/GitHub", key=f"proj_link_{i}",
                                         placeholder="https://github.com/...")
            
            projects.append({
                'name': proj_name,
                'description': proj_desc,
                'technologies': proj_tech,
                'link': proj_link
            })
            st.markdown("---")
        
        # Internships Section (Optional)
        st.markdown('<p class="section-header">💼 Internships (Optional)</p>', unsafe_allow_html=True)
        internships = []
        for i in range(st.session_state.num_internships):
            st.markdown(f"**Internship {i+1}**")
            col1, col2, col3 = st.columns(3)
            with col1:
                int_company = st.text_input(f"Company Name", key=f"int_company_{i}")
            with col2:
                int_duration = st.text_input(f"Duration", key=f"int_duration_{i}",
                                            placeholder="e.g., 3 months")
            with col3:
                int_skills = st.text_input(f"Skills Used", key=f"int_skills_{i}",
                                          placeholder="e.g., Python, Django")
            
            internships.append({
                'company': int_company,
                'duration': int_duration,
                'skills': int_skills
            })
            st.markdown("---")
        
        # Submit button
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            submit = st.form_submit_button("Create Profile", use_container_width=True)
        
        if submit:
            # Validation
            if not all([full_name, headline, college_name, branch, current_semester, skills]):
                st.error("❌ Please fill all required fields marked with *")
                return
            
            if not projects[0]['name']:
                st.error("❌ Please add at least one project")
                return
            
            # Update profile photo if uploaded
            if profile_photo:
                photo_bytes = profile_photo.getvalue()
                db.update_profile_photo(st.session_state.user['id'], photo_bytes)
                # Update session state immediately
                st.session_state.user['profile_photo'] = photo_bytes
            
            # Create student profile
            success = prof_ops.create_student_profile(
                st.session_state.user['id'],
                headline, college_name, branch, current_semester, skills
            )
            
            if success:
                # Add projects
                for proj in projects:
                    if proj['name']:
                        prof_ops.add_project(
                            st.session_state.user['id'],
                            proj['name'], proj['description'],
                            proj['technologies'], proj['link']
                        )
                
                # Add internships
                for intern in internships:
                    if intern['company']:
                        prof_ops.add_internship(
                            st.session_state.user['id'],
                            intern['company'], intern['duration'], intern['skills']
                        )
                
                st.success("✅ Profile created successfully!")
                st.session_state.profile_created = True
                st.rerun()
    
    # Show continue button after profile creation
    if st.session_state.get('profile_created', False):
        st.markdown("---")
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("Continue to Home", use_container_width=True):
                st.session_state.page = 'home'
                st.session_state.profile_created = False
                st.rerun()
    
    # Add project button (outside form)
    if not st.session_state.get('profile_created', False):
        if st.button("➕ Add Another Project"):
            st.session_state.num_projects += 1
            st.rerun()
        
        if st.button("➕ Add Internship"):
            st.session_state.num_internships += 1
            st.rerun()

if __name__ == "__main__":
    show_create_student_profile()