from database import Database
from typing import List, Dict
import notification_operations as notif_ops

db = Database()

# Like Operations
def add_like(post_id: int, user_id: int) -> bool:
    """Add a like to a post"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO likes (post_id, user_id) VALUES (?, ?)', (post_id, user_id))
        conn.commit()
        
        # Get post owner
        cursor.execute('SELECT user_id FROM posts WHERE id = ?', (post_id,))
        post_owner = cursor.fetchone()
        conn.close()
        
        # Send notification to post owner
        if post_owner and post_owner[0] != user_id:
            user = db.get_user_by_id(user_id)
            notif_ops.create_notification(
                post_owner[0], 
                user_id, 
                'like', 
                f"{user['full_name']} liked your post",
                post_id
            )
        
        return True
    except:
        return False

def remove_like(post_id: int, user_id: int) -> bool:
    """Remove a like from a post"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM likes WHERE post_id = ? AND user_id = ?', (post_id, user_id))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def get_like_count(post_id: int) -> int:
    """Get number of likes for a post"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM likes WHERE post_id = ?', (post_id,))
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except:
        return 0

def has_user_liked(post_id: int, user_id: int) -> bool:
    """Check if user has liked a post"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM likes WHERE post_id = ? AND user_id = ?', (post_id, user_id))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except:
        return False

def get_users_who_liked(post_id: int) -> List[Dict]:
    """Get list of users who liked a post"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT u.id, u.full_name, u.profile_photo
            FROM likes l
            JOIN users u ON l.user_id = u.id
            WHERE l.post_id = ?
            ORDER BY l.created_at DESC
        ''', (post_id,))
        users = cursor.fetchall()
        conn.close()
        
        return [{
            'id': u[0],
            'full_name': u[1],
            'profile_photo': u[2]
        } for u in users]
    except:
        return []

# Comment Operations
def add_comment(post_id: int, user_id: int, comment_text: str) -> bool:
    """Add a comment to a post"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO comments (post_id, user_id, comment_text)
            VALUES (?, ?, ?)
        ''', (post_id, user_id, comment_text))
        conn.commit()
        
        # Get post owner
        cursor.execute('SELECT user_id FROM posts WHERE id = ?', (post_id,))
        post_owner = cursor.fetchone()
        conn.close()
        
        # Send notification to post owner
        if post_owner and post_owner[0] != user_id:
            user = db.get_user_by_id(user_id)
            notif_ops.create_notification(
                post_owner[0], 
                user_id, 
                'comment', 
                f"{user['full_name']} commented on your post",
                post_id
            )
        
        return True
    except:
        return False

def get_comment_count(post_id: int) -> int:
    """Get number of comments for a post"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM comments WHERE post_id = ?', (post_id,))
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except:
        return 0

def get_comments(post_id: int) -> List[Dict]:
    """Get all comments for a post"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.id, c.comment_text, c.created_at, u.id, u.full_name, u.profile_photo
            FROM comments c
            JOIN users u ON c.user_id = u.id
            WHERE c.post_id = ?
            ORDER BY c.created_at ASC
        ''', (post_id,))
        comments = cursor.fetchall()
        conn.close()
        
        return [{
            'id': c[0],
            'comment_text': c[1],
            'created_at': c[2],
            'user_id': c[3],
            'user_name': c[4],
            'user_photo': c[5]
        } for c in comments]
    except:
        return []

# Follower Operations
def send_follow_request(follower_id: int, following_id: int) -> bool:
    """Send a follow request"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO followers (follower_id, following_id, status)
            VALUES (?, ?, ?)
        ''', (follower_id, following_id, 'pending'))
        conn.commit()
        conn.close()
        
        # Send notification
        user = db.get_user_by_id(follower_id)
        notif_ops.create_notification(
            following_id, 
            follower_id, 
            'follow', 
            f"{user['full_name']} wants to follow you"
        )
        
        return True
    except:
        return False

def accept_follow_request(follower_id: int, following_id: int) -> bool:
    """Accept a follow request"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE followers SET status = 'accepted' 
            WHERE follower_id = ? AND following_id = ?
        ''', (follower_id, following_id))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def get_follower_count(user_id: int) -> int:
    """Get number of followers"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM followers 
            WHERE following_id = ? AND status = 'accepted'
        ''', (user_id,))
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except:
        return 0

def get_following_count(user_id: int) -> int:
    """Get number of users this user is following"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM followers 
            WHERE follower_id = ? AND status = 'accepted'
        ''', (user_id,))
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except:
        return 0

def is_following(follower_id: int, following_id: int) -> tuple[bool, str]:
    """Check if user is following another user"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT status FROM followers 
            WHERE follower_id = ? AND following_id = ?
        ''', (follower_id, following_id))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return True, result[0]
        return False, 'not_following'
    except:
        return False, 'error'

def get_followers(user_id: int) -> List[Dict]:
    """Get list of followers"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT u.id, u.full_name, u.profile_photo, u.profile_type
            FROM followers f
            JOIN users u ON f.follower_id = u.id
            WHERE f.following_id = ? AND f.status = 'accepted'
            ORDER BY f.created_at DESC
        ''', (user_id,))
        followers = cursor.fetchall()
        conn.close()
        
        return [{
            'id': f[0],
            'full_name': f[1],
            'profile_photo': f[2],
            'profile_type': f[3]
        } for f in followers]
    except:
        return []

def get_following(user_id: int) -> List[Dict]:
    """Get list of users this user is following"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT u.id, u.full_name, u.profile_photo, u.profile_type
            FROM followers f
            JOIN users u ON f.following_id = u.id
            WHERE f.follower_id = ? AND f.status = 'accepted'
            ORDER BY f.created_at DESC
        ''', (user_id,))
        following = cursor.fetchall()
        conn.close()
        
        return [{
            'id': f[0],
            'full_name': f[1],
            'profile_photo': f[2],
            'profile_type': f[3]
        } for f in following]
    except:
        return []