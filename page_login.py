import streamlit as st
from database import Database
from validation import validate_email

db = Database()

def show_login():
    """Modern login page with professional design"""
    st.markdown("""
        <style>
        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        .login-container {
            background: white;
            padding: 50px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            max-width: 500px;
            margin: 80px auto;
        }
        
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
            font-size: 20px;
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
        
        .welcome-back {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }
        
        .welcome-text {
            color: #2c3e50;
            font-size: 18px;
            font-weight: 600;
            margin: 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Center layout
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        st.markdown('<p class="main-title">🔗 job & skills matching platform</p>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Welcome Back!</p>', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="welcome-back">
                <p class="welcome-text">👋 Great to see you again!</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<p class="form-section-title">Login to Your Account</p>', unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input("📧 Email Address", placeholder="yourname@gmail.com")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("🚀 Login")
            
            if submit:
                # Validate email format
                email_valid, email_msg = validate_email(email)
                if not email_valid:
                    st.error(f"❌ {email_msg}")
                    st.stop()
                
                # Verify credentials
                success, user_data = db.verify_user(email, password)
                
                if success:
                    st.success("✅ Login Successful!")
                    st.session_state.user = user_data
                    st.session_state.login_success = True
                    st.rerun()
                else:
                    st.error("❌ Invalid email or password. Please check your credentials.")
        
        # Show continue button
        if st.session_state.get('login_success', False):
            st.markdown('<div class="divider">───────────</div>', unsafe_allow_html=True)
            if st.button("✨ Continue", use_container_width=True):
                if st.session_state.user['profile_type'] == 'pending':
                    st.session_state.page = 'profile_type_selection'
                else:
                    st.session_state.page = 'home'
                st.session_state.login_success = False
                st.rerun()
        
        # Signup link
        st.markdown('<div class="divider">───────────</div>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #7f8c8d; font-size: 14px;">Don\'t have an account?</p>', 
                   unsafe_allow_html=True)
        
        if st.button("✍️ Sign Up Here", use_container_width=True, key="signup_link"):
            st.session_state.page = 'signin'
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    if 'page' not in st.session_state:
        st.session_state.page = 'login'
    show_login()