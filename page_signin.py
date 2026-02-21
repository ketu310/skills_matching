import streamlit as st
from database import Database
from validation import validate_email, validate_password, validate_full_name

db = Database()

def show_signin():
    """Modern sign-in page with professional design"""
    st.markdown("""
        <style>
        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        # .signin-container {
        #     background: white;
        #     padding: 50px;
        #     border-radius: 20px;
        #     box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        #     max-width: 500px;
        #     margin: 50px auto;
        # }
        
        .main-title {
            text-align: center;
            background: linear-gradient(90deg, #0077B5 0%, #00A0DC 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 48px;
            font-weight: 800;
            margin-bottom: 10px;
        }
        
        .subtitle {
            text-align: center;
            color: #7f8c8d;
            font-size: 18px;
            margin-bottom: 40px;
            font-weight: 500;
        }
        
        .form-section-title {
            color: #2c3e50;
            font-size: 28px;
            font-weight: 700;
            text-align: center;
            margin-bottom: 30px;
        }
        
        .stTextInput > label {
            color: #2c3e50;
            font-weight: 600;
            font-size: 14px;
        }
        
        .stTextInput > div > div > input {
            border: 2px solid #e1e8ed;
            border-radius: 10px;
            padding: 12px;
            font-size: 15px;
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #0077B5;
            box-shadow: 0 0 0 3px rgba(0, 119, 181, 0.1);
        }
        
        .stButton > button {
            background: linear-gradient(90deg, #0077B5 0%, #00A0DC 100%);
            color: white;
            border-radius: 12px;
            height: 50px;
            font-size: 16px;
            font-weight: 700;
            border: none;
            width: 100%;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 119, 181, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 119, 181, 0.4);
        }
        
        .divider {
            text-align: center;
            margin: 30px 0;
            color: #95a5a6;
            font-size: 14px;
        }
        
        .secondary-btn {
            background: white !important;
            color: #0077B5 !important;
            border: 2px solid #0077B5 !important;
        }
        
        .feature-box {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 4px solid #0077B5;
        }
        
        .feature-title {
            color: #2c3e50;
            font-weight: 600;
            font-size: 16px;
            margin-bottom: 8px;
        }
        
        .feature-text {
            color: #7f8c8d;
            font-size: 14px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Center layout
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # st.markdown('<div class="signin-container">', unsafe_allow_html=True)
        
        st.markdown('<p class="main-title">🔗 job & skills matching platform</p>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Connect. Grow. Succeed.</p>', unsafe_allow_html=True)
        
        st.markdown('<p class="form-section-title">Create Your Account</p>', unsafe_allow_html=True)
        
        with st.form("signin_form", clear_on_submit=False):
            full_name = st.text_input("✨ Full Name", placeholder="John Doe")
            email = st.text_input("📧 Email Address", placeholder="yourname@gmail.com")
            password = st.text_input("🔒 Password", type="password", 
                                    placeholder="Min 8 chars, with A-Z, a-z, 0-9, symbols")
            confirm_password = st.text_input("🔑 Confirm Password", type="password", 
                                           placeholder="Re-enter your password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("🚀 Create Account")
            
            if submit:
                # Validate full name
                name_valid, name_msg = validate_full_name(full_name)
                if not name_valid:
                    st.error(f"❌ {name_msg}")
                    st.stop()
                
                # Validate email
                email_valid, email_msg = validate_email(email)
                if not email_valid:
                    st.error(f"❌ {email_msg}")
                    st.stop()
                
                # Check if email exists
                if db.email_exists(email):
                    st.error("❌ Email already exists. Please login instead.")
                    st.stop()
                
                # Validate password
                pwd_valid, pwd_msg = validate_password(password)
                if not pwd_valid:
                    st.error(f"❌ {pwd_msg}")
                    st.stop()
                
                # Check password confirmation
                if password != confirm_password:
                    st.error("❌ Passwords do not match")
                    st.stop()
                
                # Create user
                success, message = db.create_user(full_name, email, password)
                
                if success:
                    st.success("✅ Account Created Successfully!")
                    st.session_state.signin_email = email
                    st.session_state.signin_password = password
                    st.session_state.show_continue = True
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
        
        # Show continue button
        if st.session_state.get('show_continue', False):
            st.markdown('<div class="divider">───────────</div>', unsafe_allow_html=True)
            if st.button("✨ Continue to Profile Setup", use_container_width=True):
                success, user_data = db.verify_user(
                    st.session_state.signin_email, 
                    st.session_state.signin_password
                )
                if success:
                    st.session_state.user = user_data
                    st.session_state.page = 'profile_type_selection'
                    st.session_state.show_continue = False
                    st.rerun()
        
        # Login link
        st.markdown('<div class="divider">───────────</div>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #7f8c8d; font-size: 14px;">Already have an account?</p>', 
                   unsafe_allow_html=True)
        
        if st.button("🔐 Login Here", use_container_width=True, key="login_link"):
            st.session_state.page = 'login'
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Features
        st.markdown("""
            <div class="feature-box">
                <div class="feature-title">🎯 Why Join LinkedIn Mini?</div>
                <div class="feature-text">
                    ✓ Connect with professionals worldwide<br>
                    ✓ Find your dream job with AI matching<br>
                    ✓ Showcase your skills and projects<br>
                    ✓ Network with top companies
                </div>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    if 'page' not in st.session_state:
        st.session_state.page = 'signin'
    show_signin()