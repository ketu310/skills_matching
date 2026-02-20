
import streamlit as st
import post_operations as post_ops
import job_operations as job_ops
import profile_operations as prof_ops
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import base64

def show_jobs():
    """Jobs page for students and employees with clean, professional design"""
    
    # Clean, professional styling
    st.markdown("""
        <style>
        /* Main background */
        .main {
            background: #f5f7fa;
        }
        
        /* Job card */
        .job-card {
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin: 15px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border-left: 4px solid #0077B5;
        }
        
        .job-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        }
        
        /* Match badge */
        .match-badge {
            display: inline-block;
            padding: 6px 14px;
            border-radius: 15px;
            font-weight: 700;
            font-size: 13px;
            margin-left: 10px;
        }
        
        .match-high {
            background: #28a745;
            color: white;
        }
        
        .match-medium {
            background: #ffc107;
            color: #333;
        }
        
        .match-low {
            background: #6c757d;
            color: white;
        }
        
        /* Company logo */
        .company-logo {
            width: 60px;
            height: 60px;
            border-radius: 8px;
            overflow: hidden;
            border: 2px solid #e9ecef;
            display: flex;
            align-items: center;
            justify-content: center;
            background: white;
        }
        
        .company-logo img {
            width: 100%;
            height: 100%;
            object-fit: cover;
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
        }
        </style>
    """, unsafe_allow_html=True)
    
    if st.button("⬅ Back to Home"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown("# 💼 Jobs")
    
    tab1, tab2, tab3 = st.tabs(["📌 Recommended Jobs", "📋 All Jobs", "✅ Applied Jobs"])
    
    # Get user skills and experience
    user_skills = ""
    user_exp = 0
    if st.session_state.user['profile_type'] == 'student':
        profile = prof_ops.get_student_profile(st.session_state.user['id'])
        user_skills = profile.get('skills', '') if profile else ''
        user_exp = 0
    else:
        profile = prof_ops.get_employee_profile(st.session_state.user['id'])
        user_skills = profile.get('skills', '') if profile else ''
        user_exp = profile.get('years_of_experience', 0) if profile else 0
    
    all_jobs = post_ops.get_all_company_job_posts()
    
    with tab1:
        st.markdown("### Jobs matching your profile (60%+)")
        recommended = []
        for job in all_jobs:
            match = job_ops.calculate_match_score(user_skills, user_exp, job['required_skills'], job.get('experience', '0'))
            if match['overall_match'] >= 60:
                job['match_score'] = match
                recommended.append(job)
        
        # Sort by match score
        recommended.sort(key=lambda x: x['match_score']['overall_match'], reverse=True)
        
        if not recommended:
            st.info("🔍 No recommended jobs at this time. Check 'All Jobs' tab!")
        else:
            for job in recommended:
                display_job(job, True, "rec")
    
    with tab2:
        st.markdown("### All Available Jobs")
        for job in all_jobs:
            match = job_ops.calculate_match_score(user_skills, user_exp, job['required_skills'], job.get('experience', '0'))
            job['match_score'] = match
            display_job(job, True, "all")
    
    with tab3:
        st.markdown("### Your Applications")
        applications = job_ops.get_user_applications(st.session_state.user['id'])
        
        if not applications:
            st.info("📝 You haven't applied to any jobs yet")
        else:
            for app in applications:
                st.markdown('<div class="job-card">', unsafe_allow_html=True)
                st.markdown(f"### 💼 {app['job_title']}")
                st.markdown(f"**🏢 Company:** {app['company_name']}")
                
                status_colors = {
                    'pending': '🟡',
                    'accepted': '🟢',
                    'rejected': '🔴'
                }
                st.markdown(f"**Status:** {status_colors.get(app['status'], '⚪')} {app['status'].title()}")
                st.markdown(f"**📅 Applied on:** {app['created_at']}")
                st.markdown('</div>', unsafe_allow_html=True)

def display_job(job, show_apply=True, tab_prefix=""):
    """Display a job posting with clean card design"""
    
    st.markdown('<div class="job-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 10])
    
    with col1:
        try:
            if job.get('company_logo'):
                img = Image.open(BytesIO(job['company_logo']))
                img_b64 = base64.b64encode(job['company_logo']).decode()
                st.markdown(f"""
                    <div class="company-logo">
                        <img src="data:image/png;base64,{img_b64}" />
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown('<div class="company-logo">🏢</div>', unsafe_allow_html=True)
        except:
            st.markdown('<div class="company-logo">🏢</div>', unsafe_allow_html=True)
    
    with col2:
        # Job title with match badge
        match_score = job.get('match_score', {}).get('overall_match', 0)
        
        if match_score >= 80:
            badge_class = 'match-high'
            badge_text = 'Excellent Match'
        elif match_score >= 60:
            badge_class = 'match-medium'
            badge_text = 'Good Match'
        else:
            badge_class = 'match-low'
            badge_text = 'Fair Match'
        
        st.markdown(f"""
            <h3 style='margin-bottom: 5px;'>💼 {job['job_title']} 
            <span class='match-badge {badge_class}'>{match_score:.0f}% {badge_text}</span>
            </h3>
        """, unsafe_allow_html=True)
        
        st.markdown(f"**🏢 {job['company_name']}** | 📍 {job['job_location']} | 🕒 {job['job_type']}")
        
        if st.button("👁️ View Details", key=f"{tab_prefix}_view_job_{job['id']}"):
            st.session_state.view_job_id = job['id']
            st.session_state.expanded_job = True
            st.session_state.expanded_tab = tab_prefix
            st.rerun()
        
        if (st.session_state.get('view_job_id') == job['id'] and 
            st.session_state.get('expanded_job') and 
            st.session_state.get('expanded_tab') == tab_prefix):
            
            match_score_obj = job.get('match_score', {})
            
            st.markdown("---")
            
            # Skills breakdown
            st.markdown("#### 🎯 Skills Match Analysis")
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown("**✅ Matched Skills**")
                matched_skills = match_score_obj.get('matched_skills', [])
                if matched_skills:
                    for skill in matched_skills:
                        st.markdown(f"• {skill}")
                else:
                    st.markdown("*None*")
            
            with col_b:
                st.markdown("**❌ Missing Skills**")
                missing_skills = match_score_obj.get('missing_skills', [])
                if missing_skills:
                    for skill in missing_skills:
                        st.markdown(f"• {skill}")
                else:
                    st.markdown("*None*")
            
            # Experience comparison
            st.markdown("#### 📊 Experience Requirements")
            col_exp1, col_exp2 = st.columns(2)
            with col_exp1:
                st.metric("Required Experience", f"{match_score_obj.get('required_experience', 0)} years")
            with col_exp2:
                st.metric("Your Experience", f"{match_score_obj.get('user_experience', 0)} years")
            
            # VERTICAL Bar chart
            st.markdown("#### 📈 Skills Breakdown Chart")
            
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
            
            # Job description
            st.markdown("#### 📝 Job Description")
            st.markdown(job['job_description'])
            
            if show_apply:
                # Check if already applied or employed
                already_applied = job_ops.has_applied(st.session_state.user['id'], job['id'])
                is_employee = job_ops.is_employee(job['user_id'], st.session_state.user['id'])
                
                if is_employee:
                    st.success("✅ You are already in this company")
                elif already_applied:
                    st.info("⏳ Application pending")
                else:
                    if st.button("📤 Apply Now", key=f"{tab_prefix}_apply_{job['id']}"):
                        success, msg = job_ops.apply_for_job(st.session_state.user['id'], job['id'], job['user_id'])
                        if success:
                            st.success("✅ " + msg)
                        else:
                            st.error(msg)
                        st.rerun()
            
            if st.button("❌ Close Details", key=f"{tab_prefix}_close_{job['id']}"):
                st.session_state.expanded_job = False
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    show_jobs()