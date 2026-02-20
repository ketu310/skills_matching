import streamlit as st
from database import Database

db = Database()

def show_profile_type_selection():
    """Display profile type selection page"""
    st.markdown("""
        <style>
        .main-title {
            text-align: center;
            color: #0077B5;
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 40px;
        }
        .stButton > button {
            width: 100%;
            background-color: #0077B5;
            color: white;
            border-radius: 24px;
            height: 48px;
            font-size: 16px;
            font-weight: 600;
            border: none;
        }
        .stButton > button:hover {
            background-color: #006399;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="main-title">Select Your Profile Type</p>', unsafe_allow_html=True)
    
    # Center the selection
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Choose the option that best describes you:")
        
        profile_type = st.radio(
            "Profile Type",
            options=["Student", "Employee", "Company/Recruiter"],
            index=0,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        if st.button("Continue", use_container_width=True):
            # Update profile type in database
            user_id = st.session_state.user['id']
            
            if profile_type == "Student":
                db.update_profile_type(user_id, 'student')
                st.session_state.user['profile_type'] = 'student'
                st.session_state.page = 'create_student_profile'
            elif profile_type == "Employee":
                db.update_profile_type(user_id, 'employee')
                st.session_state.user['profile_type'] = 'employee'
                st.session_state.page = 'create_employee_profile'
            else:
                db.update_profile_type(user_id, 'company')
                st.session_state.user['profile_type'] = 'company'
                st.session_state.page = 'create_company_profile'
            
            st.rerun()

if __name__ == "__main__":
    show_profile_type_selection()