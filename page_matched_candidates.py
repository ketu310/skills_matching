
import streamlit as st
import post_operations as post_ops
import job_operations as job_ops
import profile_operations as prof_ops
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import base64

def show_matched_candidates():
    """Matched candidates page for companies with clean, professional design"""
    
    # Clean, professional styling
    st.markdown("""
        <style>
        /* Main background */
        .main {
            background: #f5f7fa;
        }
        
        /* Candidate card */
        .candidate-card {
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin: 15px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border-left: 4px solid #0077B5;
        }
        
        .candidate-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        }
        
        /* Match score badge */
        .match-score {
            display: inline-block;
            background: #0077B5;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 16px;
            font-weight: 700;
        }
        
        /* Profile photo in matched candidates */
        .candidate-photo {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            overflow: hidden;
            border: 3px solid #0077B5;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
            justify-content: center;
            background: white;
        }
        
        .candidate-photo img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        .default-candidate-avatar {
            width: 80px;
            height: 80px;
            background: #0077B5;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 40px;
            color: white;
            border: 3px solid #0077B5;
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
        
        /* Section headers */
        h3 {
            color: #2c3e50;
            border-bottom: 2px solid #0077B5;
            padding-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    if st.button("⬅ Back to Home"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown("# 🎯 Matched Candidates")
    
    tab1, tab2 = st.tabs(["📊 Candidate Matches", "📨 Applications Received"])
    
    with tab1:
        show_candidate_matches()
    
    with tab2:
        show_applications_received()

def show_candidate_matches():
    """Show candidates matched with company job posts"""
    st.markdown("### Candidates Matching Your Job Posts")
    
    # Get company's job posts
    job_posts = post_ops.get_company_job_posts(st.session_state.user['id'])
    
    if not job_posts:
        st.info("📝 Post jobs to see matched candidates")
        return
    
    # Get all job seeking posts
    job_seekers = post_ops.get_all_job_seeking_posts(st.session_state.user['id'])
    
    from database import Database
    db = Database()
    
    for job_post in job_posts:
        st.markdown(f"### 💼 {job_post['job_title']}")
        
        matched_candidates = []
        for seeker in job_seekers:
            # Get seeker's experience
            seeker_exp = 0
            if seeker.get('profile_type') == 'employee':
                profile = prof_ops.get_employee_profile(seeker['user_id'])
                seeker_exp = profile.get('years_of_experience', 0) if profile else 0
            
            # Calculate match
            match = job_ops.calculate_match_score(
                seeker['required_skills'], 
                seeker_exp,
                job_post['required_skills'],
                job_post.get('experience', '0')
            )
            
            if match['overall_match'] >= 60:
                # Get user data with profile photo
                user_data = db.get_user_by_id(seeker['user_id'])
                matched_candidates.append({
                    'seeker': seeker,
                    'match': match,
                    'user_data': user_data
                })
        
        if not matched_candidates:
            st.info("🔍 No matching candidates yet")
        else:
            for item in matched_candidates:
                seeker = item['seeker']
                match = item['match']
                user_data = item['user_data']
                
                st.markdown('<div class="candidate-card">', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([1, 4, 2])
                
                with col1:
                    # Display user profile photo
                    try:
                        if user_data and user_data.get('profile_photo'):
                            img_b64 = base64.b64encode(user_data['profile_photo']).decode()
                            st.markdown(f"""
                                <div class="candidate-photo">
                                    <img src="data:image/png;base64,{img_b64}" />
                                </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="default-candidate-avatar">👤</div>', unsafe_allow_html=True)
                    except:
                        st.markdown('<div class="default-candidate-avatar">👤</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"**👤 {seeker['user_name']}**")
                    st.markdown(f"<span class='match-score'>Match: {match['overall_match']:.1f}%</span>", unsafe_allow_html=True)
                
                with col3:
                    if st.button("View Details", key=f"view_match_{seeker['id']}"):
                        st.session_state.view_match_seeker = seeker
                        st.session_state.view_match_score = match
                        st.rerun()
                
                # Show details if selected
                if st.session_state.get('view_match_seeker', {}).get('id') == seeker['id']:
                    show_match_details(seeker, match)
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")

def show_match_details(seeker, match):
    """Show detailed match breakdown with VERTICAL bar chart"""
    st.markdown("---")
    st.markdown(f"**🎯 Role:** {seeker['role_domain']}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### ✅ Matched Skills")
        matched_skills = match.get('matched_skills', [])
        if matched_skills:
            for skill in matched_skills:
                st.markdown(f"• {skill}")
        else:
            st.markdown("*None*")
    
    with col2:
        st.markdown("#### ❌ Missing Skills")
        missing_skills = match.get('missing_skills', [])
        if missing_skills:
            for skill in missing_skills:
                st.markdown(f"• {skill}")
        else:
            st.markdown("*None*")
    
    # VERTICAL Bar chart
    st.markdown("#### 📊 Skills Breakdown")
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    categories = ['Matched\nSkills', 'Missing\nSkills']
    values = [len(matched_skills), len(missing_skills)]
    colors = ['#0077B5', '#FF6B6B']
    
    # Create VERTICAL bar chart
    bars = ax.bar(categories, values, color=colors, width=0.5, edgecolor='white', linewidth=2)
    
    # Add value labels on top of bars
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(val)}',
                ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    ax.set_ylabel('Number of Skills', fontsize=11, fontweight='bold')
    ax.set_title('Skills Match Analysis', fontsize=13, fontweight='bold', pad=15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_ylim(0, max(values) * 1.2 if max(values) > 0 else 5)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    # Check if already approached
    is_employee = job_ops.is_employee(st.session_state.user['id'], seeker['user_id'])
    
    if is_employee:
        st.success("✅ Already in your company")
    else:
        if st.button("📧 Approach Candidate", key=f"approach_matched_{seeker['id']}"):
            success, msg = job_ops.approach_candidate(
                st.session_state.user['id'], 
                seeker['user_id'], 
                seeker['id']
            )
            if success:
                st.success("✅ " + msg)
            else:
                st.error(msg)
            st.rerun()

def show_applications_received():
    """Show applications received for company job posts"""
    st.markdown("### Applications Received")
    
    from database import Database
    db = Database()
    
    # Get all applications for this company
    conn = job_ops.db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT ja.id, ja.user_id, ja.post_id, ja.status, ja.created_at,
               u.full_name, p.job_title
        FROM job_applications ja
        JOIN users u ON ja.user_id = u.id
        JOIN posts p ON ja.post_id = p.id
        WHERE ja.company_id = ?
        ORDER BY ja.created_at DESC
    ''', (st.session_state.user['id'],))
    applications = cursor.fetchall()
    conn.close()
    
    if not applications:
        st.info("📭 No applications received yet")
        return
    
    for app in applications:
        app_id, user_id, post_id, status, created_at, user_name, job_title = app
        
        # Get user data for profile photo
        user_data = db.get_user_by_id(user_id)
        
        st.markdown('<div class="candidate-card">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 5, 2])
        
        with col1:
            # Display user profile photo
            try:
                if user_data and user_data.get('profile_photo'):
                    img_b64 = base64.b64encode(user_data['profile_photo']).decode()
                    st.markdown(f"""
                        <div class="candidate-photo">
                            <img src="data:image/png;base64,{img_b64}" />
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown('<div class="default-candidate-avatar">👤</div>', unsafe_allow_html=True)
            except:
                st.markdown('<div class="default-candidate-avatar">👤</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"**👤 {user_name}**")
            st.markdown(f"Applied for: **💼 {job_title}**")
            st.caption(f"Status: {status.title()} | 📅 {created_at}")
        
        with col3:
            if status == 'pending':
                if st.button("✅ Accept", key=f"accept_app_{app_id}"):
                    success, msg = job_ops.accept_job_application(app_id)
                    if success:
                        st.success("✅ " + msg)
                    else:
                        st.error(msg)
                    st.rerun()
            elif status == 'accepted':
                st.success("✅ Accepted")
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    show_matched_candidates()