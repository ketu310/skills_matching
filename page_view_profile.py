import streamlit as st
from database import Database
import profile_operations as prof_ops
import post_operations as post_ops
import interaction_operations as inter_ops
from PIL import Image
from io import BytesIO

db = Database()

def show_view_profile():
    """View another user's profile"""
    if st.button("⬅ Back"):
        st.session_state.page = 'home'
        st.rerun()
    
    user_id = st.session_state.get('view_user_id')
    if not user_id:
        st.error("User not found")
        return
    
    user = db.get_user_by_id(user_id)
    if not user:
        st.error("User not found")
        return
    
    # Profile header
    col1, col2 = st.columns([1, 4])
    with col1:
        try:
            if user.get('profile_photo'):
                st.image(Image.open(BytesIO(user['profile_photo'])), width=150)
            else:
                st.markdown("# 👤")
        except:
            st.markdown("# 👤")
    
    with col2:
        st.markdown(f"# {user['full_name']}")
        st.markdown(f"**Profile Type:** {user['profile_type'].title()}")
    
    # Display profile based on type
    if user['profile_type'] == 'student':
        profile = prof_ops.get_student_profile(user_id)
        if profile:
            st.markdown(f"**{profile['headline']}**")
            st.markdown(f"🎓 **{profile['college_name']}** - {profile['branch']}")
            st.markdown(f"📚 {profile['current_semester']}")
            st.markdown(f"**Skills:** {profile['skills']}")
        
        projects = prof_ops.get_projects(user_id)
        if projects:
            st.markdown("### 🚀 Projects")
            for proj in projects:
                st.markdown(f"**{proj['project_name']}**")
                st.markdown(f"{proj['description']}")
                st.markdown(f"*Technologies: {proj['technologies']}*")
                if proj['project_link']:
                    st.markdown(f"[Link]({proj['project_link']})")
                st.markdown("---")
    
    elif user['profile_type'] == 'employee':
        profile = prof_ops.get_employee_profile(user_id)
        if profile:
            st.markdown(f"**{profile['headline']}**")
            st.markdown(f"💼 {profile['job_title']} at {profile['company_name']}")
            st.markdown(f"🏢 {profile['industry']}")
            st.markdown(f"📅 {profile['years_of_experience']} years experience")
            st.markdown(f"**Skills:** {profile['skills']}")
    
    elif user['profile_type'] == 'company':
        profile = prof_ops.get_company_profile(user_id)
        if profile:
            st.markdown(f"📍 **Location:** {profile['location']}")
            st.markdown(f"**About:** {profile['description']}")
    
    # Show user's posts
    st.markdown("### 📝 Posts")
    posts = post_ops.get_user_normal_posts(user_id)
    for idx, post in enumerate(posts):
        display_post(post, user, True, idx)

def display_post(post, user, allow_interaction=True, post_idx=0):
    """Display a single post with like/comment"""
    with st.container():
        col1, col2 = st.columns([1, 10])
        with col1:
            try:
                if user.get('profile_photo'):
                    st.image(Image.open(BytesIO(user['profile_photo'])), width=50)
                else:
                    st.markdown("👤")
            except:
                st.markdown("👤")
        with col2:
            st.markdown(f"**{user['full_name']}**")
            st.markdown(post['content'])
            
            if post.get('file_data') and post.get('file_type'):
                if 'image' in post['file_type']:
                    try:
                        st.image(Image.open(BytesIO(post['file_data'])))
                    except:
                        pass
        
        if allow_interaction:
            likes = inter_ops.get_like_count(post['id'])
            comments = inter_ops.get_comment_count(post['id'])
            has_liked = inter_ops.has_user_liked(post['id'], st.session_state.user['id'])
            
            col1, col2, col3 = st.columns([1, 1, 8])
            with col1:
                if has_liked:
                    if st.button(f"❤️ {likes}", key=f"vp_unlike_{post_idx}_{post['id']}"):
                        inter_ops.remove_like(post['id'], st.session_state.user['id'])
                        st.rerun()
                else:
                    if st.button(f"🤍 {likes}", key=f"vp_like_{post_idx}_{post['id']}"):
                        inter_ops.add_like(post['id'], st.session_state.user['id'])
                        st.rerun()
            
            with col2:
                st.markdown(f"💬 {comments}")
            
            # Comment section
            all_comments = inter_ops.get_comments(post['id'])
            for comment in all_comments:
                st.markdown(f"**{comment['user_name']}:** {comment['comment_text']}")
            
            comment_text = st.text_input("Add comment", key=f"vp_comment_{post_idx}_{post['id']}")
            if st.button("Post Comment", key=f"vp_post_comment_{post_idx}_{post['id']}"):
                if comment_text:
                    inter_ops.add_comment(post['id'], st.session_state.user['id'], comment_text)
                    st.rerun()
        
        st.markdown("---")