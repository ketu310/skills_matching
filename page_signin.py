# import streamlit as st
# from database import Database
# from validation import validate_email, validate_password, validate_full_name

# db = Database()

# def show_signin():
#     """Modern sign-in page with professional design"""
#     st.markdown("""
#         <style>
#         .main {
#             background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         }
        
#         # .signin-container {
#         #     background: white;
#         #     padding: 50px;
#         #     border-radius: 20px;
#         #     box-shadow: 0 10px 40px rgba(0,0,0,0.2);
#         #     max-width: 500px;
#         #     margin: 50px auto;
#         # }
        
#         .main-title {
#             text-align: center;
#             background: linear-gradient(90deg, #0077B5 0%, #00A0DC 100%);
#             -webkit-background-clip: text;
#             -webkit-text-fill-color: transparent;
#             font-size: 48px;
#             font-weight: 800;
#             margin-bottom: 10px;
#         }
        
#         .subtitle {
#             text-align: center;
#             color: #7f8c8d;
#             font-size: 18px;
#             margin-bottom: 40px;
#             font-weight: 500;
#         }
        
#         .form-section-title {
#             color: #2c3e50;
#             font-size: 28px;
#             font-weight: 700;
#             text-align: center;
#             margin-bottom: 30px;
#         }
        
#         .stTextInput > label {
#             color: #2c3e50;
#             font-weight: 600;
#             font-size: 14px;
#         }
        
#         .stTextInput > div > div > input {
#             border: 2px solid #e1e8ed;
#             border-radius: 10px;
#             padding: 12px;
#             font-size: 15px;
#             transition: all 0.3s ease;
#         }
        
#         .stTextInput > div > div > input:focus {
#             border-color: #0077B5;
#             box-shadow: 0 0 0 3px rgba(0, 119, 181, 0.1);
#         }
        
#         .stButton > button {
#             background: linear-gradient(90deg, #0077B5 0%, #00A0DC 100%);
#             color: white;
#             border-radius: 12px;
#             height: 50px;
#             font-size: 16px;
#             font-weight: 700;
#             border: none;
#             width: 100%;
#             transition: all 0.3s ease;
#             box-shadow: 0 4px 15px rgba(0, 119, 181, 0.3);
#         }
        
#         .stButton > button:hover {
#             transform: translateY(-2px);
#             box-shadow: 0 6px 20px rgba(0, 119, 181, 0.4);
#         }
        
#         .divider {
#             text-align: center;
#             margin: 30px 0;
#             color: #95a5a6;
#             font-size: 14px;
#         }
        
#         .secondary-btn {
#             background: white !important;
#             color: #0077B5 !important;
#             border: 2px solid #0077B5 !important;
#         }
        
#         .feature-box {
#             background: #f8f9fa;
#             padding: 20px;
#             border-radius: 10px;
#             margin: 20px 0;
#             border-left: 4px solid #0077B5;
#         }
        
#         .feature-title {
#             color: #2c3e50;
#             font-weight: 600;
#             font-size: 16px;
#             margin-bottom: 8px;
#         }
        
#         .feature-text {
#             color: #7f8c8d;
#             font-size: 14px;
#         }
#         </style>
#     """, unsafe_allow_html=True)
    
#     # Center layout
#     col1, col2, col3 = st.columns([1, 3, 1])
    
#     with col2:
#         # st.markdown('<div class="signin-container">', unsafe_allow_html=True)
        
#         st.markdown('<p class="main-title">🔗 LinkedIn Mini</p>', unsafe_allow_html=True)
#         st.markdown('<p class="subtitle">Connect. Grow. Succeed.</p>', unsafe_allow_html=True)
        
#         st.markdown('<p class="form-section-title">Create Your Account</p>', unsafe_allow_html=True)
        
#         with st.form("signin_form", clear_on_submit=False):
#             full_name = st.text_input("✨ Full Name", placeholder="John Doe")
#             email = st.text_input("📧 Email Address", placeholder="yourname@gmail.com")
#             password = st.text_input("🔒 Password", type="password", 
#                                     placeholder="Min 8 chars, with A-Z, a-z, 0-9, symbols")
#             confirm_password = st.text_input("🔑 Confirm Password", type="password", 
#                                            placeholder="Re-enter your password")
            
#             st.markdown("<br>", unsafe_allow_html=True)
#             submit = st.form_submit_button("🚀 Create Account")
            
#             if submit:
#                 # Validate full name
#                 name_valid, name_msg = validate_full_name(full_name)
#                 if not name_valid:
#                     st.error(f"❌ {name_msg}")
#                     st.stop()
                
#                 # Validate email
#                 email_valid, email_msg = validate_email(email)
#                 if not email_valid:
#                     st.error(f"❌ {email_msg}")
#                     st.stop()
                
#                 # Check if email exists
#                 if db.email_exists(email):
#                     st.error("❌ Email already exists. Please login instead.")
#                     st.stop()
                
#                 # Validate password
#                 pwd_valid, pwd_msg = validate_password(password)
#                 if not pwd_valid:
#                     st.error(f"❌ {pwd_msg}")
#                     st.stop()
                
#                 # Check password confirmation
#                 if password != confirm_password:
#                     st.error("❌ Passwords do not match")
#                     st.stop()
                
#                 # Create user
#                 success, message = db.create_user(full_name, email, password)
                
#                 if success:
#                     st.success("✅ Account Created Successfully!")
#                     st.session_state.signin_email = email
#                     st.session_state.signin_password = password
#                     st.session_state.show_continue = True
#                     st.rerun()
#                 else:
#                     st.error(f"❌ {message}")
        
#         # Show continue button
#         if st.session_state.get('show_continue', False):
#             st.markdown('<div class="divider">───────────</div>', unsafe_allow_html=True)
#             if st.button("✨ Continue to Profile Setup", use_container_width=True):
#                 success, user_data = db.verify_user(
#                     st.session_state.signin_email, 
#                     st.session_state.signin_password
#                 )
#                 if success:
#                     st.session_state.user = user_data
#                     st.session_state.page = 'profile_type_selection'
#                     st.session_state.show_continue = False
#                     st.rerun()
        
#         # Login link
#         st.markdown('<div class="divider">───────────</div>', unsafe_allow_html=True)
#         st.markdown('<p style="text-align: center; color: #7f8c8d; font-size: 14px;">Already have an account?</p>', 
#                    unsafe_allow_html=True)
        
#         if st.button("🔐 Login Here", use_container_width=True, key="login_link"):
#             st.session_state.page = 'login'
#             st.rerun()
        
#         st.markdown('</div>', unsafe_allow_html=True)
        
#         # Features
#         st.markdown("""
#             <div class="feature-box">
#                 <div class="feature-title">🎯 Why Join LinkedIn Mini?</div>
#                 <div class="feature-text">
#                     ✓ Connect with professionals worldwide<br>
#                     ✓ Find your dream job with AI matching<br>
#                     ✓ Showcase your skills and projects<br>
#                     ✓ Network with top companies
#                 </div>
#             </div>
#         """, unsafe_allow_html=True)

# if __name__ == "__main__":
#     if 'page' not in st.session_state:
#         st.session_state.page = 'signin'
#     show_signin()

import streamlit as st
from database import Database
from validation import validate_email, validate_password, validate_full_name

db = Database()

def show_signin():
    """Professional sign-in page for AI Powered Job & Skills Matching Platform"""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

        /* ── Base ── */
        html, body,
        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewContainer"] > .main {
            background: #ffffff !important;
            font-family: 'Inter', sans-serif;
        }

        [data-testid="block-container"] {
            padding: 0 1rem 3rem !important;
            max-width: 100% !important;
        }

        #MainMenu, footer, header { visibility: hidden; }

        /* ══════════════════════════════════════
           TOP HERO BANNER
        ══════════════════════════════════════ */
        .hero-banner {
            width: 100%;
            background: linear-gradient(135deg, #0a1628 0%, #0d2147 40%, #0a3880 70%, #1a5ccc 100%);
            padding: 52px 24px 44px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        /* subtle dot grid overlay */
        .hero-banner::before {
            content: '';
            position: absolute;
            inset: 0;
            background-image: radial-gradient(circle, rgba(255,255,255,0.07) 1px, transparent 1px);
            background-size: 28px 28px;
        }

        /* soft glow behind title */
        .hero-banner::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 600px;
            height: 200px;
            background: radial-gradient(ellipse, rgba(96,165,250,0.18) 0%, transparent 70%);
            pointer-events: none;
        }

        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.18);
            border-radius: 100px;
            padding: 5px 16px;
            margin-bottom: 22px;
            position: relative;
            z-index: 2;
        }
        .hero-badge span {
            font-size: 11px;
            font-weight: 500;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: rgba(255,255,255,0.75);
        }
        .badge-dot {
            width: 6px; height: 6px;
            border-radius: 50%;
            background: #60a5fa;
            animation: pulse 2s ease infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50%       { opacity: 0.5; transform: scale(1.6); }
        }

        .project-title {
            font-family: 'Sora', sans-serif;
            font-size: clamp(26px, 4.5vw, 48px);
            font-weight: 800;
            line-height: 1.15;
            letter-spacing: -0.5px;
            position: relative;
            z-index: 2;
            margin-bottom: 14px;
        }
        .title-accent {
            display: block;
            background: linear-gradient(90deg, #60a5fa 0%, #a78bfa 60%, #93c5fd 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .title-main {
            display: block;
            color: #ffffff;
        }

        .hero-tagline {
            position: relative;
            z-index: 2;
            font-size: 15px;
            font-weight: 300;
            color: rgba(255,255,255,0.5);
            letter-spacing: 0.2px;
            margin-top: 4px;
        }
        .hero-tagline em {
            color: rgba(147,197,253,0.85);
            font-style: normal;
            font-weight: 500;
        }

        /* ══════════════════════════════════════
           CONNECTOR
        ══════════════════════════════════════ */
        .connector {
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .connector-line-l {
            flex: 1;
            height: 1px;
            background: linear-gradient(90deg, transparent, #bfdbfe);
        }
        .connector-line-r {
            flex: 1;
            height: 1px;
            background: linear-gradient(90deg, #bfdbfe, transparent);
        }
        .connector-diamond {
            width: 10px; height: 10px;
            background: #3b82f6;
            transform: rotate(45deg);
            margin: 0 12px;
            box-shadow: 0 0 0 4px rgba(59,130,246,0.15);
        }

        /* ══════════════════════════════════════
           FORM OUTER GLOW RING
        ══════════════════════════════════════ */
        .form-outer {
            position: relative;
            border-radius: 24px;
            padding: 3px;
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #06b6d4 100%);
            box-shadow:
                0 24px 64px rgba(59,130,246,0.16),
                0 8px 24px rgba(0,0,0,0.07);
            animation: fadeUp 0.65s ease both;
        }
        @keyframes fadeUp {
            from { opacity: 0; transform: translateY(18px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        /* corner bracket accents */
        .form-outer::before,
        .form-outer::after {
            content: '';
            position: absolute;
            width: 56px; height: 56px;
            pointer-events: none;
            z-index: 3;
        }
        .form-outer::before {
            top: -6px; left: -6px;
            border-top: 2.5px solid rgba(59,130,246,0.45);
            border-left: 2.5px solid rgba(59,130,246,0.45);
            border-radius: 6px 0 0 0;
        }
        .form-outer::after {
            bottom: -6px; right: -6px;
            border-bottom: 2.5px solid rgba(139,92,246,0.45);
            border-right: 2.5px solid rgba(139,92,246,0.45);
            border-radius: 0 0 6px 0;
        }

        .form-inner-top {
            background: #ffffff;
            border-radius: 22px 22px 0 0;
            padding: 36px 36px 20px;
        }
        .form-inner-bottom {
            background: #ffffff;
            border-radius: 0 0 22px 22px;
            padding: 0 36px 32px;
        }

        .form-header-title {
            font-family: 'Sora', sans-serif;
            font-size: 20px;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 4px;
        }
        .form-header-sub {
            font-size: 13px;
            color: #94a3b8;
            margin-bottom: 0;
        }

        /* ── Original form input style ── */
        .stTextInput > label {
            color: #2c3e50 !important;
            font-weight: 600 !important;
            font-size: 14px !important;
        }
        .stTextInput > div > div > input {
            border: 2px solid #e1e8ed !important;
            border-radius: 10px !important;
            padding: 12px !important;
            font-size: 15px !important;
            transition: all 0.3s ease !important;
        }
        .stTextInput > div > div > input:focus {
            border-color: #0077B5 !important;
            box-shadow: 0 0 0 3px rgba(0, 119, 181, 0.1) !important;
        }

        /* ── Original button style ── */
        .stButton > button {
            background: linear-gradient(90deg, #0077B5 0%, #00A0DC 100%) !important;
            color: white !important;
            border-radius: 12px !important;
            height: 50px !important;
            font-size: 16px !important;
            font-weight: 700 !important;
            border: none !important;
            width: 100% !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(0, 119, 181, 0.3) !important;
        }
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(0, 119, 181, 0.4) !important;
        }

        /* ── Divider ── */
        .divider {
            text-align: center;
            margin: 30px 0;
            color: #95a5a6;
            font-size: 14px;
        }

        /* ── Feature box (original style) ── */
        .feature-box {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0 0;
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
            line-height: 1.8;
        }

        .page-footer {
            text-align: center;
            margin-top: 28px;
            font-size: 12px;
            color: #cbd5e1;
        }
        </style>

        <!-- HERO BANNER -->
        <div class="hero-banner">
            <div class="hero-badge">
                <div class="badge-dot"></div>
                <span>AI Powered Platform</span>
            </div>
            <div class="project-title">
                <span class="title-accent">AI Powered Job &amp; Skills</span>
                <span class="title-main">Matching Platform</span>
            </div>
            <div class="hero-tagline">
                Find your perfect role with <em>intelligent matching</em> technology
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ── Layout ──
    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:

        # Connector
        st.markdown("""
            <div style="height:32px;"></div>
            <div class="connector">
                <div class="connector-line-l"></div>
                <div class="connector-diamond"></div>
                <div class="connector-line-r"></div>
            </div>
            <div style="height:20px;"></div>
        """, unsafe_allow_html=True)

        # Glow ring top half + title
        st.markdown("""
            <div class="form-outer">
                <div class="form-inner-top">
                    <div class="form-header-title">Create Your Account</div>
                    <div class="form-header-sub">Join professionals finding their perfect job match</div>
                </div>
                <div class="form-inner-bottom">
        """, unsafe_allow_html=True)

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
                name_valid, name_msg = validate_full_name(full_name)
                if not name_valid:
                    st.error(f"❌ {name_msg}")
                    st.stop()

                email_valid, email_msg = validate_email(email)
                if not email_valid:
                    st.error(f"❌ {email_msg}")
                    st.stop()

                if db.email_exists(email):
                    st.error("❌ Email already exists. Please login instead.")
                    st.stop()

                pwd_valid, pwd_msg = validate_password(password)
                if not pwd_valid:
                    st.error(f"❌ {pwd_msg}")
                    st.stop()

                if password != confirm_password:
                    st.error("❌ Passwords do not match")
                    st.stop()

                success, message = db.create_user(full_name, email, password)

                if success:
                    st.success("✅ Account Created Successfully!")
                    st.session_state.signin_email = email
                    st.session_state.signin_password = password
                    st.session_state.show_continue = True
                    st.rerun()
                else:
                    st.error(f"❌ {message}")

        # Close glow ring
        st.markdown("</div></div>", unsafe_allow_html=True)

        # Continue button
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

        # Feature box
        st.markdown("""
            <div class="feature-box">
                <div class="feature-title">🎯 Why Join Our Platform?</div>
                <div class="feature-text">
                    ✓ Connect with professionals worldwide<br>
                    ✓ Find your dream job with AI matching<br>
                    ✓ Showcase your skills and projects<br>
                    ✓ Network with top companies
                </div>
            </div>
            <div class="page-footer">© 2025 AI Powered Job &amp; Skills Matching Platform</div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    if 'page' not in st.session_state:
        st.session_state.page = 'signin'
    show_signin()