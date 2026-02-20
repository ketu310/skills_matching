import streamlit as st
from database import Database

# Import all pages
import page_signin
import page_login
import page_profile_type_selection

# Initialize database
db = Database()

# Page configuration
st.set_page_config(
    page_title="LinkedIn Mini",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'signin'

if 'user' not in st.session_state:
    st.session_state.user = None

# Main routing logic
def main():
    """Main application router"""
    
    # If user is not logged in
    if st.session_state.user is None:
        if st.session_state.page == 'login':
            page_login.show_login()
        else:
            page_signin.show_signin()
    
    # If user is logged in but profile type not selected
    elif st.session_state.user['profile_type'] == 'pending':
        page_profile_type_selection.show_profile_type_selection()
    
    # User is fully set up
    else:
        # Import profile and home pages
        if st.session_state.page == 'create_student_profile':
            import page_create_student_profile
            page_create_student_profile.show_create_student_profile()
        
        elif st.session_state.page == 'create_employee_profile':
            import page_create_employee_profile
            page_create_employee_profile.show_create_employee_profile()
        
        elif st.session_state.page == 'create_company_profile':
            import page_create_company_profile
            page_create_company_profile.show_create_company_profile()
        
        elif st.session_state.page == 'home':
            import page_home
            page_home.show_home()
        
        elif st.session_state.page == 'view_profile':
            import page_view_profile
            page_view_profile.show_view_profile()
        
        elif st.session_state.page == 'edit_profile':
            import page_edit_profile
            page_edit_profile.show_edit_profile()
        
        elif st.session_state.page == 'jobs':
            import page_jobs
            page_jobs.show_jobs()
        
        elif st.session_state.page == 'post':
            import page_post
            page_post.show_post()
        
        elif st.session_state.page == 'notifications':
            import page_notifications
            page_notifications.show_notifications()
        
        elif st.session_state.page == 'matched_candidates':
            import page_matched_candidates
            page_matched_candidates.show_matched_candidates()
        
        else:
            # Default to home
            import page_home
            page_home.show_home()

if __name__ == "__main__":
    main()