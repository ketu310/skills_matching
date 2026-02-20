import streamlit as st
from database import Database
import profile_operations as prof_ops
from PIL import Image

db = Database()

def show_create_company_profile():
    """Company profile creation page"""
    st.markdown('<style>.profile-title{color:#0077B5;font-size:32px;font-weight:bold;}.section-header{color:#0077B5;font-size:22px;font-weight:600;margin-top:20px;border-bottom:2px solid #0077B5;padding-bottom:10px;}</style>', unsafe_allow_html=True)
    
    st.markdown('<p class="profile-title">🏢 Create Company Profile</p>', unsafe_allow_html=True)
    
    with st.form("company_profile_form"):
        st.markdown('<p class="section-header">🏢 Company Basic Info</p>', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 3])
        
        with col1:
            logo = st.file_uploader("Company Logo", type=['png', 'jpg', 'jpeg'])
            if logo:
                st.image(Image.open(logo), width=150)
        
        with col2:
            company_name = st.text_input("Company Name*", value=st.session_state.user['full_name'])
            location = st.text_input("Location*", placeholder="e.g., San Francisco, CA")
        
        st.markdown('<p class="section-header">📝 About Company</p>', unsafe_allow_html=True)
        description = st.text_area("Company Description*", 
                                  placeholder="What does your company do? What are your main products/services?",
                                  height=150)
        
        submit = st.form_submit_button("Create Profile", use_container_width=True)
        
        if submit:
            if not all([company_name, location, description]):
                st.error("❌ Please fill all required fields")
                return
            
            if logo:
                logo_bytes = logo.getvalue()
                db.update_profile_photo(st.session_state.user['id'], logo_bytes)
                st.session_state.user['profile_photo'] = logo_bytes
            
            success = prof_ops.create_company_profile(
                st.session_state.user['id'], location, description
            )
            
            if success:
                st.success("✅ Company profile created successfully!")
                st.session_state.profile_created = True
                st.rerun()
    
    if st.session_state.get('profile_created', False):
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("Continue to Home", use_container_width=True):
                st.session_state.page = 'home'
                st.session_state.profile_created = False
                st.rerun()