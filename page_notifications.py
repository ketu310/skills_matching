
import streamlit as st
import notification_operations as notif_ops
import interaction_operations as inter_ops
import job_operations as job_ops
from database import Database
from io import BytesIO
from PIL import Image
import base64

db = Database()

def show_notifications():
    """Beautiful, modern notifications page"""
    
    # Stunning modern design
    st.markdown("""
        <style>
        /* Main background with gradient */
        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        /* Notification card */
        .notif-card {
            background: white;
            border-radius: 15px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            border-left: 5px solid #0077B5;
            position: relative;
            overflow: hidden;
        }
        
        .notif-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        
        /* Unread notification - more prominent */
        .notif-card.unread {
            border-left: 5px solid #FF6B6B;
            background: linear-gradient(135deg, #fff 0%, #fff5f5 100%);
        }
        
        .notif-card.unread::before {
            content: "NEW";
            position: absolute;
            top: 10px;
            right: 10px;
            background: #FF6B6B;
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.5px;
        }
        
        /* Read notification - subtle */
        .notif-card.read {
            opacity: 0.8;
            border-left: 5px solid #95a5a6;
        }
        
        /* Notification type badges */
        .notif-type {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 15px;
            font-size: 12px;
            font-weight: 700;
            margin-right: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .notif-type.follow {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
        }
        
        .notif-type.job {
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            color: white;
        }
        
        .notif-type.approach {
            background: linear-gradient(135deg, #30cfd0 0%, #330867 100%);
            color: white;
        }
        
        .notif-type.like {
            background: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%);
            color: white;
        }
        
        .notif-type.comment {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        /* User avatar in notification */
        .notif-avatar {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            overflow: hidden;
            border: 3px solid #0077B5;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            display: flex;
            align-items: center;
            justify-content: center;
            background: white;
        }
        
        .notif-avatar img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        .default-notif-avatar {
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 25px;
            color: white;
            border: 3px solid #0077B5;
        }
        
        /* Notification message */
        .notif-message {
            font-size: 15px;
            color: #2c3e50;
            line-height: 1.6;
            margin: 8px 0;
        }
        
        .notif-message.unread {
            font-weight: 600;
            color: #1a1a1a;
        }
        
        /* Timestamp */
        .notif-time {
            font-size: 13px;
            color: #7f8c8d;
            font-style: italic;
        }
        
        /* Action buttons */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px 20px;
            font-weight: 700;
            transition: all 0.3s ease;
            box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }
        
        /* Header */
        .notif-header {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 25px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        }
        
        .notif-header h1 {
            color: white;
            margin: 0;
            font-size: 32px;
            font-weight: 800;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        .notif-stats {
            color: white;
            margin-top: 10px;
            font-size: 16px;
            opacity: 0.9;
        }
        
        /* Empty state */
        .empty-notif {
            background: white;
            border-radius: 15px;
            padding: 60px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .empty-notif-icon {
            font-size: 80px;
            margin-bottom: 20px;
            opacity: 0.6;
        }
        
        .empty-notif-text {
            font-size: 20px;
            color: #7f8c8d;
            font-weight: 500;
        }
        </style>
    """, unsafe_allow_html=True)
    
    if st.button("⬅ Back to Home"):
        st.session_state.page = 'home'
        st.rerun()
    
    # Get notifications
    notifications = notif_ops.get_notifications(st.session_state.user['id'])
    unread_count = sum(1 for n in notifications if not n['is_read'])
    
    # Header with stats
    st.markdown(f"""
        <div class="notif-header">
            <h1>🔔 Notifications</h1>
            <p class="notif-stats">
                {len(notifications)} total notifications | 
                <span style="color: #FF6B6B; font-weight: 700;">{unread_count} unread</span>
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Mark all as read button
    if unread_count > 0:
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("✓ Mark All as Read", use_container_width=True):
                for notif in notifications:
                    if not notif['is_read']:
                        notif_ops.mark_as_read(notif['id'])
                st.success("✅ All notifications marked as read!")
                st.rerun()
    
    if not notifications:
        st.markdown("""
            <div class="empty-notif">
                <div class="empty-notif-icon">🔕</div>
                <p class="empty-notif-text">No notifications yet</p>
                <p style="color: #95a5a6; margin-top: 10px;">You're all caught up!</p>
            </div>
        """, unsafe_allow_html=True)
        return
    
    # Display notifications
    for notif in notifications:
        # Get user data for avatar
        try:
            from_user = db.get_user_by_id(notif['from_user_id'])
        except:
            from_user = None
        
        # Determine card class based on read status
        card_class = "unread" if not notif['is_read'] else "read"
        
        # Determine notification type badge
        notif_type_map = {
            'follow': ('follow', '👥 Follow Request'),
            'job_application': ('job', '💼 Job Application'),
            'company_approach': ('approach', '🏢 Company Approach'),
            'like': ('like', '❤️ Like'),
            'comment': ('comment', '💬 Comment'),
            'application_accepted': ('job', '✅ Accepted'),
            'approach_accepted': ('approach', '✅ Accepted')
        }
        
        type_class, type_label = notif_type_map.get(notif['notification_type'], ('follow', '📢 Notification'))
        
        st.markdown(f'<div class="notif-card {card_class}">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 6, 2])
        
        with col1:
            # Display user avatar
            try:
                if from_user and from_user.get('profile_photo'):
                    img_b64 = base64.b64encode(from_user['profile_photo']).decode()
                    st.markdown(f"""
                        <div class="notif-avatar">
                            <img src="data:image/png;base64,{img_b64}" />
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown('<div class="default-notif-avatar">👤</div>', unsafe_allow_html=True)
            except:
                st.markdown('<div class="default-notif-avatar">👤</div>', unsafe_allow_html=True)
        
        with col2:
            # Notification type badge
            st.markdown(f'<span class="notif-type {type_class}">{type_label}</span>', unsafe_allow_html=True)
            
            # Message
            message_class = "unread" if not notif['is_read'] else ""
            st.markdown(f'<p class="notif-message {message_class}">{notif["message"]}</p>', unsafe_allow_html=True)
            
            # Timestamp
            st.markdown(f'<p class="notif-time">🕐 {notif["created_at"]}</p>', unsafe_allow_html=True)
        
        with col3:
            # Action buttons based on notification type
            if notif['notification_type'] == 'follow' and not notif['is_read']:
                if st.button("✅ Accept", key=f"accept_follow_{notif['id']}", use_container_width=True):
                    inter_ops.accept_follow_request(notif['from_user_id'], st.session_state.user['id'])
                    notif_ops.mark_as_read(notif['id'])
                    st.success("✅ Follow request accepted!")
                    st.rerun()
            
            elif notif['notification_type'] == 'job_application' and not notif['is_read']:
                if st.button("👁️ View", key=f"view_app_{notif['id']}", use_container_width=True):
                    st.session_state.page = 'matched_candidates'
                    notif_ops.mark_as_read(notif['id'])
                    st.rerun()
            
            elif notif['notification_type'] == 'company_approach' and not notif['is_read']:
                # Get approach ID
                approaches = job_ops.get_company_approaches(st.session_state.user['id'])
                for app in approaches:
                    if app['company_id'] == notif['from_user_id'] and app['status'] == 'pending':
                        if st.button("✅ Accept", key=f"accept_approach_{notif['id']}", use_container_width=True):
                            success, msg = job_ops.accept_company_approach(app['id'])
                            if success:
                                st.success("✅ " + msg)
                                notif_ops.mark_as_read(notif['id'])
                                st.rerun()
                        break
            
            # Mark as read button for all notifications
            if not notif['is_read']:
                if st.button("✓", key=f"mark_read_{notif['id']}", help="Mark as read"):
                    notif_ops.mark_as_read(notif['id'])
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    show_notifications()