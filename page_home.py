
import streamlit as st
from database import Database
import profile_operations as prof_ops
import interaction_operations as inter_ops
import notification_operations as notif_ops
from PIL import Image
from io import BytesIO
import base64

db = Database()

def show_home():
    """Home page with modern professional design"""
    
    # Advanced CSS styling with improved design
    st.markdown("""
        <style>
        /* Global Styles */
        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 0;
        }
        
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }
        
        /* Top Header Bar */
        .top-header {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            padding: 25px 40px;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
        }
        
        .header-title {
            color: white;
            font-size: 32px;
            font-weight: 800;
            margin: 0;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
            letter-spacing: -0.5px;
        }
        
        /* Profile Photo Circle - FIXED */
        .profile-header-container {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .profile-photo-circle {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            overflow: hidden;
            border: 3px solid white;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            background: white;
            flex-shrink: 0;
        }
        
        .profile-photo-circle img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        .default-avatar-header {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
            color: white;
            border: 3px solid white;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        
        /* Search Bar Styling */
        .stTextInput > div > div > input {
            background-color: rgba(255, 255, 255, 0.95);
            border: none;
            border-radius: 30px;
            padding: 15px 25px;
            font-size: 16px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .stTextInput > div > div > input:focus {
            background-color: white;
            box-shadow: 0 6px 25px rgba(0,0,0,0.15);
            transform: translateY(-2px);
        }
        
        /* Selectbox styling */
        .stSelectbox > div > div {
            background-color: white;
            border-radius: 15px;
            box-shadow: 0 3px 15px rgba(0,0,0,0.08);
        }
        
        /* Navigation Bar */
        .nav-container {
            background: white;
            padding: 20px 25px;
            border-radius: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        
        /* User Card Design */
        .user-card {
            background: white;
            border-radius: 20px;
            padding: 30px;
            margin: 20px 0;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            border: 1px solid #e9ecef;
        }
        
        .user-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 35px rgba(0,0,0,0.15);
            border-color: #667eea;
        }
        
        .user-name {
            color: #2c3e50;
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 8px;
            line-height: 1.3;
        }
        
        .user-headline {
            color: #6c757d;
            font-size: 15px;
            margin-bottom: 12px;
            line-height: 1.5;
        }
        
        .user-stats {
            color: #667eea;
            font-size: 14px;
            font-weight: 600;
        }
        
        /* Profile Photo in Card - FIXED */
        .card-profile-photo {
            width: 90px;
            height: 90px;
            border-radius: 50%;
            overflow: hidden;
            border: 4px solid #667eea;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            background: white;
        }
        
        .card-profile-photo img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        .default-avatar-card {
            width: 90px;
            height: 90px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 45px;
            color: white;
            border: 4px solid #667eea;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
        }
        
        /* Button Styling */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 12px 28px;
            font-weight: 700;
            font-size: 15px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            letter-spacing: 0.3px;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
        }
        
        /* Badge Styles */
        .badge {
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 700;
            margin-left: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .badge-student {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            box-shadow: 0 2px 8px rgba(79, 172, 254, 0.4);
        }
        
        .badge-employee {
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            color: white;
            box-shadow: 0 2px 8px rgba(250, 112, 154, 0.4);
        }
        
        .badge-company {
            background: linear-gradient(135deg, #30cfd0 0%, #330867 100%);
            color: white;
            box-shadow: 0 2px 8px rgba(48, 207, 208, 0.4);
        }
        
        /* Section Headers */
        .section-header {
            color: white;
            font-size: 28px;
            font-weight: 800;
            margin: 35px 0 25px 0;
            padding: 20px 30px;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 80px 30px;
            background: white;
            border-radius: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }
        
        .empty-state-icon {
            font-size: 80px;
            margin-bottom: 25px;
            filter: grayscale(0.3);
        }
        
        .empty-state-text {
            color: #6c757d;
            font-size: 20px;
            font-weight: 500;
        }
        
        /* Following Status */
        .status-following {
            color: #28a745;
            font-weight: 700;
            padding: 8px 16px;
            background: #d4edda;
            border-radius: 10px;
            display: inline-block;
            margin-top: 10px;
        }
        
        .status-pending {
            color: #ffc107;
            font-weight: 700;
            padding: 8px 16px;
            background: #fff3cd;
            border-radius: 10px;
            display: inline-block;
            margin-top: 10px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Refresh user data from database
    current_user = db.get_user_by_id(st.session_state.user['id'])
    if current_user:
        st.session_state.user = current_user
    
    # Top Header with Logo, Search, and Profile
    col_logo, col_search, col_profile = st.columns([2, 5, 3])
    
    with col_logo:
        st.markdown('<div class="top-header"><p class="header-title">🔗 job & skills matching platform</p></div>', unsafe_allow_html=True)
    
    with col_search:
        st.markdown("<div style='padding-top: 8px;'>", unsafe_allow_html=True)
        search_query = st.text_input("🔍 Search users", "", key="search_bar", label_visibility="collapsed", placeholder="Search professionals, companies...")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col_profile:
        st.markdown("<div style='padding-top: 15px;'>", unsafe_allow_html=True)
        
        # Profile header with photo and edit button
        prof_col1, prof_col2 = st.columns([1, 2])
        
        with prof_col1:
            try:
                if st.session_state.user.get('profile_photo'):
                    img = Image.open(BytesIO(st.session_state.user['profile_photo']))
                    # Create circular image using HTML/CSS
                    st.markdown(f"""
                        <div class="profile-photo-circle">
                            <img src="data:image/png;base64,{base64.b64encode(st.session_state.user['profile_photo']).decode()}" />
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown('<div class="default-avatar-header">👤</div>', unsafe_allow_html=True)
            except:
                st.markdown('<div class="default-avatar-header">👤</div>', unsafe_allow_html=True)
        
        with prof_col2:
            if st.button("✏️ Edit Profile", key="edit_profile_btn", use_container_width=True):
                st.session_state.page = 'edit_profile'
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Navigation Bar
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    
    if st.session_state.user['profile_type'] == 'company':
        col1, col2, col3, col4 = st.columns(4)
    else:
        col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🏠 Home", key="nav_home", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
    
    if st.session_state.user['profile_type'] == 'company':
        with col2:
            if st.button("🎯 Matched Candidates", key="nav_matched", use_container_width=True):
                st.session_state.page = 'matched_candidates'
                st.rerun()
    else:
        with col2:
            if st.button("💼 Jobs", key="nav_jobs", use_container_width=True):
                st.session_state.page = 'jobs'
                st.rerun()
    
    with col3:
        if st.button("📝 Posts", key="nav_post", use_container_width=True):
            st.session_state.page = 'post'
            st.rerun()
    
    with col4:
        unread = notif_ops.get_unread_count(st.session_state.user['id'])
        notif_label = f"🔔 Notifications ({unread})" if unread > 0 else "🔔 Notifications"
        if st.button(notif_label, key="nav_notif", use_container_width=True):
            st.session_state.page = 'notifications'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Dropdown Filter instead of buttons
    st.markdown("<br>", unsafe_allow_html=True)
    
    filter_col1, filter_col2 = st.columns([2, 8])
    
    with filter_col1:
        filter_options = {
            "👥 All Users": "all",
            "🎓 Students": "student",
            "💼 Employees": "employee",
            "🏢 Companies": "company"
        }
        
        # Initialize filter if not exists
        if 'user_filter' not in st.session_state:
            st.session_state.user_filter = 'all'
        
        # Get current filter display name
        current_filter_name = [k for k, v in filter_options.items() if v == st.session_state.user_filter][0]
        
        selected_filter = st.selectbox(
            "Filter Users",
            options=list(filter_options.keys()),
            index=list(filter_options.values()).index(st.session_state.user_filter),
            key="filter_dropdown"
        )
        
        # Update filter
        st.session_state.user_filter = filter_options[selected_filter]
    
    # Display current filter header
    filter_labels = {
        'all': '👥 All Users',
        'student': '🎓 Students',
        'employee': '💼 Employees',
        'company': '🏢 Companies'
    }
    
    st.markdown(f'<p class="section-header">{filter_labels.get(st.session_state.user_filter, "👥 All Users")}</p>', unsafe_allow_html=True)
    
    # Get users based on filter
    if search_query:
        users = db.search_users(search_query)
    else:
        users = db.get_all_users(st.session_state.user['id'])
    
    # Filter users by category
    if st.session_state.user_filter != 'all':
        users = [u for u in users if u['profile_type'] == st.session_state.user_filter]
    
    if not users:
        st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">🔍</div>
                <p class="empty-state-text">No users found in this category</p>
            </div>
        """, unsafe_allow_html=True)
        return
    
    # Display users in modern cards
    for user in users:
        with st.container():
            st.markdown('<div class="user-card">', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 5, 2])
            
            with col1:
                try:
                    if user.get('profile_photo'):
                        # Use base64 encoding for proper circular display
                        img_b64 = base64.b64encode(user['profile_photo']).decode()
                        st.markdown(f"""
                            <div class="card-profile-photo">
                                <img src="data:image/png;base64,{img_b64}" />
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="default-avatar-card">👤</div>', unsafe_allow_html=True)
                except:
                    st.markdown('<div class="default-avatar-card">👤</div>', unsafe_allow_html=True)
            
            with col2:
                # Get badge class based on profile type
                badge_class = f"badge-{user['profile_type']}"
                type_emoji = {"student": "🎓", "employee": "💼", "company": "🏢"}
                
                st.markdown(f"""
                    <p class="user-name">
                        {user['full_name']}
                        <span class="badge {badge_class}">
                            {type_emoji.get(user['profile_type'], '👤')} {user['profile_type'].title()}
                        </span>
                    </p>
                """, unsafe_allow_html=True)
                
                # Get headline
                headline = ""
                if user['profile_type'] == 'student':
                    profile = prof_ops.get_student_profile(user['id'])
                    if profile:
                        headline = profile.get('headline', '')
                elif user['profile_type'] == 'employee':
                    profile = prof_ops.get_employee_profile(user['id'])
                    if profile:
                        headline = profile.get('headline', '')
                else:
                    profile = prof_ops.get_company_profile(user['id'])
                    if profile:
                        headline = profile.get('location', 'Company')
                
                if headline:
                    st.markdown(f'<p class="user-headline">{headline}</p>', unsafe_allow_html=True)
                
                # Follower count
                followers = inter_ops.get_follower_count(user['id'])
                st.markdown(f'<p class="user-stats">👥 {followers} followers</p>', unsafe_allow_html=True)
            
            with col3:
                st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
                
                if st.button("👁️ View Profile", key=f"view_{user['id']}", use_container_width=True):
                    st.session_state.view_user_id = user['id']
                    st.session_state.page = 'view_profile'
                    st.rerun()
                
                is_follow, status = inter_ops.is_following(st.session_state.user['id'], user['id'])
                if is_follow and status == 'accepted':
                    st.markdown('<p class="status-following">✓ Following</p>', unsafe_allow_html=True)
                elif is_follow and status == 'pending':
                    st.markdown('<p class="status-pending">⏳ Pending</p>', unsafe_allow_html=True)
                else:
                    if st.button("➕ Follow", key=f"follow_{user['id']}", use_container_width=True):
                        inter_ops.send_follow_request(st.session_state.user['id'], user['id'])
                        st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    show_home()