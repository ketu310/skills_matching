
import streamlit as st
import post_operations as post_ops
import interaction_operations as inter_ops
import profile_operations as prof_ops
from PIL import Image
from io import BytesIO
import base64

def show_post():
    """Post page with different sections based on user type"""
    
    # Styling for posts
    st.markdown("""
        <style>
        /* Main background */
        .main {
            background: #f5f7fa;
        }
        
        /* Post card */
        .post-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        
        /* User profile photo in posts */
        .post-user-photo {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            overflow: hidden;
            border: 2px solid #0077B5;
            display: flex;
            align-items: center;
            justify-content: center;
            background: white;
        }
        
        .post-user-photo img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        .default-post-avatar {
            width: 50px;
            height: 50px;
            background: #0077B5;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 25px;
            color: white;
            border: 2px solid #0077B5;
        }
        
        /* Post image preview */
        .post-image-preview {
            cursor: pointer;
            border-radius: 8px;
            overflow: hidden;
            display: inline-block;
            border: 2px solid #e9ecef;
        }
        
        .post-image-preview:hover {
            border-color: #0077B5;
            transform: scale(1.02);
            transition: all 0.2s ease;
        }
        
        /* Buttons */
        .stButton > button {
            background: #0077B5;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 20px;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        
        .stButton > button:hover {
            background: #005582;
        }
        </style>
    """, unsafe_allow_html=True)
    
    if st.button("⬅ Back"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown("# 📝 Posts")
    
    user_type = st.session_state.user['profile_type']
    
    if user_type in ['student', 'employee']:
        tabs = st.tabs(["📄 Normal Post", "💼 Looking for Job/Internship", "🏢 Company Job Posts", "👥 User Posts"])
        
        with tabs[0]:
            show_normal_post_section()
        
        with tabs[1]:
            show_job_seeking_section()
        
        with tabs[2]:
            show_company_jobs_view()
        
        with tabs[3]:
            show_user_posts_section()
    
    else:  # company
        tabs = st.tabs(["📄 Normal Post", "💼 Own Job Posts", "👥 Job Seekers"])
        
        with tabs[0]:
            show_normal_post_section()
        
        with tabs[1]:
            show_own_job_posts()
        
        with tabs[2]:
            show_job_seekers()

def show_normal_post_section():
    """Create and view own normal posts"""
    st.markdown("### Create Post")
    with st.form("normal_post"):
        content = st.text_area("What's on your mind?")
        file = st.file_uploader("Upload Photo/Video", type=['png', 'jpg', 'jpeg', 'mp4', 'mov'])
        
        if st.form_submit_button("Post"):
            file_data = None
            file_type = None
            if file:
                file_data = file.getvalue()
                file_type = file.type
            
            success, msg = post_ops.create_normal_post(st.session_state.user['id'], content, file_data, file_type)
            if success:
                st.success("✅ Posted!")
                st.rerun()
    
    st.markdown("### Your Posts")
    posts = post_ops.get_user_normal_posts(st.session_state.user['id'])
    for idx, post in enumerate(posts):
        display_normal_post(post, False, f"own_{idx}")

def show_job_seeking_section():
    """Job seeking posts"""
    st.markdown("### Post Job/Internship Requirement")
    
    # Get user skills
    user_skills = ""
    if st.session_state.user['profile_type'] == 'student':
        profile = prof_ops.get_student_profile(st.session_state.user['id'])
        user_skills = profile.get('skills', '') if profile else ''
    else:
        profile = prof_ops.get_employee_profile(st.session_state.user['id'])
        user_skills = profile.get('skills', '') if profile else ''
    
    with st.form("job_seeking"):
        looking_for = st.selectbox("Looking for", ["Job", "Internship"])
        role = st.text_input("Role/Domain")
        skills = st.text_input("Skills", value=user_skills)
        location = st.text_input("Preferred Location/Remote")
        description = st.text_area("Short Description")
        
        if st.form_submit_button("Post"):
            success, msg = post_ops.create_job_seeking_post(st.session_state.user['id'], looking_for, role, skills, location, description)
            if success:
                st.success("✅ Posted!")
                st.rerun()
    
    st.markdown("### Your Job Seeking Posts")
    posts = post_ops.get_user_job_seeking_posts(st.session_state.user['id'])
    for post in posts:
        st.markdown(f"**{post['looking_for']} - {post['role_domain']}**")
        st.markdown(f"Skills: {post['required_skills']}")
        st.markdown(f"Location: {post['preferred_location']}")
        st.markdown("---")

def show_company_jobs_view():
    """View all company job posts"""
    st.markdown("### Company Job Postings")
    jobs = post_ops.get_all_company_job_posts()
    
    import job_operations as job_ops
    
    for idx, job in enumerate(jobs):
        with st.container():
            st.markdown(f"### {job['job_title']}")
            st.markdown(f"**{job['company_name']}**")
            st.markdown(f"**Location:** {job['job_location']} | **Type:** {job['job_type']}")
            
            # Check status
            already_applied = job_ops.has_applied(st.session_state.user['id'], job['id'])
            is_employee = job_ops.is_employee(job['user_id'], st.session_state.user['id'])
            
            if is_employee:
                st.success("✅ You work here")
            elif already_applied:
                st.info("⏳ Applied")
            else:
                if st.button("Apply", key=f"company_job_apply_{idx}_{job['id']}"):
                    success, msg = job_ops.apply_for_job(st.session_state.user['id'], job['id'], job['user_id'])
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
                    st.rerun()
            st.markdown("---")

def show_user_posts_section():
    """View posts from other users"""
    st.markdown("### Posts from Other Users")
    posts = post_ops.get_all_normal_posts(st.session_state.user['id'])
    
    for idx, post in enumerate(posts):
        display_normal_post(post, True, f"user_{idx}")

def show_own_job_posts():
    """Company's own job posts"""
    st.markdown("### Post a Job")
    with st.form("company_job"):
        title = st.text_input("Job Title")
        skills = st.text_input("Required Skills")
        exp = st.text_input("Experience Required")
        job_type = st.selectbox("Job Type", ["Internship", "Full-time"])
        location = st.text_input("Location/Remote")
        description = st.text_area("Job Description")
        
        if st.form_submit_button("Post Job"):
            success, msg = post_ops.create_company_job_post(st.session_state.user['id'], title, skills, exp, job_type, location, description)
            if success:
                st.success("✅ Job Posted!")
                st.rerun()
    
    st.markdown("### Your Job Posts")
    posts = post_ops.get_company_job_posts(st.session_state.user['id'])
    for post in posts:
        st.markdown(f"**{post['job_title']}**")
        st.markdown(f"Skills: {post['required_skills']}")
        st.markdown(f"Location: {post['job_location']}")
        st.markdown("---")

def show_job_seekers():
    """View job seekers for companies"""
    st.markdown("### Job Seekers")
    posts = post_ops.get_all_job_seeking_posts(st.session_state.user['id'])
    
    import job_operations as job_ops
    
    for idx, post in enumerate(posts):
        with st.container():
            st.markdown(f"### {post['user_name']} - {post['looking_for']}")
            st.markdown(f"**Role:** {post['role_domain']}")
            st.markdown(f"**Skills:** {post['required_skills']}")
            st.markdown(f"**Location:** {post['preferred_location']}")
            
            # Check status
            already_approached = job_ops.has_approached(st.session_state.user['id'], post['user_id'], post['id'])
            is_employee = job_ops.is_employee(st.session_state.user['id'], post['user_id'])
            
            if is_employee:
                st.success("✅ In your company")
            elif already_approached:
                st.info("⏳ Approached")
            else:
                if st.button("Approach", key=f"approach_seeker_{idx}_{post['id']}"):
                    success, msg = job_ops.approach_candidate(st.session_state.user['id'], post['user_id'], post['id'])
                    if success:
                        st.success("✅ " + msg)
                    else:
                        st.error(msg)
                    st.rerun()
            st.markdown("---")

def display_normal_post(post, allow_interaction, prefix=""):
    """Display a normal post with 200x200 image preview and click to view full size"""
    from database import Database
    db = Database()
    
    st.markdown('<div class="post-card">', unsafe_allow_html=True)
    
    user = db.get_user_by_id(post['user_id']) if 'user_id' in post and allow_interaction else st.session_state.user
    
    col1, col2 = st.columns([1, 10])
    with col1:
        # Display user profile photo
        try:
            if user and user.get('profile_photo'):
                img_b64 = base64.b64encode(user['profile_photo']).decode()
                st.markdown(f"""
                    <div class="post-user-photo">
                        <img src="data:image/png;base64,{img_b64}" />
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown('<div class="default-post-avatar">👤</div>', unsafe_allow_html=True)
        except:
            st.markdown('<div class="default-post-avatar">👤</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"**{user.get('full_name', 'User')}**")
        st.markdown(post.get('content', ''))
        
        # Display post image if exists
        if post.get('file_data'):
            if 'image' in post.get('file_type', ''):
                try:
                    img = Image.open(BytesIO(post['file_data']))
                    
                    # Create a unique key for this post's image
                    img_key = f"{prefix}_img_{post['id']}"
                    
                    # Check if user wants to view full size
                    if st.session_state.get(f'view_full_{img_key}', False):
                        # Show full size image
                        st.image(img, use_container_width=True)
                        if st.button("✖ Close Full View", key=f"{prefix}_close_full_{post['id']}"):
                            st.session_state[f'view_full_{img_key}'] = False
                            st.rerun()
                    else:
                        # Show 200x200 preview
                        # Resize image to 200x200 while maintaining aspect ratio
                        img.thumbnail((200, 200), Image.Resampling.LANCZOS)
                        
                        # Display preview
                        col_img, col_btn = st.columns([1, 3])
                        with col_img:
                            st.image(img, width=200)
                        with col_btn:
                            if st.button("🔍 View Full Size", key=f"{prefix}_view_full_{post['id']}"):
                                st.session_state[f'view_full_{img_key}'] = True
                                st.rerun()
                except Exception as e:
                    st.error(f"Error loading image: {str(e)}")
    
    if allow_interaction:
        likes = inter_ops.get_like_count(post['id'])
        comments_count = inter_ops.get_comment_count(post['id'])
        has_liked = inter_ops.has_user_liked(post['id'], st.session_state.user['id'])
        
        col1, col2 = st.columns([1, 5])
        with col1:
            if has_liked:
                if st.button(f"👍 {likes}", key=f"{prefix}_unlike_{post['id']}"):
                    inter_ops.remove_like(post['id'], st.session_state.user['id'])
                    st.rerun()
            else:
                if st.button(f"👍 {likes}", key=f"{prefix}_like_{post['id']}"):
                    inter_ops.add_like(post['id'], st.session_state.user['id'])
                    st.rerun()
        with col2:
            st.markdown(f"💬 {comments_count} comments")
        
        # Comments
        comments = inter_ops.get_comments(post['id'])
        for comment in comments:
            st.markdown(f"**{comment['user_name']}:** {comment['comment_text']}")
        
        comment_text = st.text_input("Comment", key=f"{prefix}_comment_input_{post['id']}")
        if st.button("Post", key=f"{prefix}_post_comment_{post['id']}"):
            if comment_text:
                inter_ops.add_comment(post['id'], st.session_state.user['id'], comment_text)
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    show_post()