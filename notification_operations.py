from database import Database
from typing import List, Dict

db = Database()

def create_notification(user_id: int, from_user_id: int, notification_type: str, 
                       message: str, post_id: int = None) -> bool:
    """Create a notification"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO notifications (user_id, from_user_id, notification_type, message, post_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, from_user_id, notification_type, message, post_id))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def get_notifications(user_id: int) -> List[Dict]:
    """Get all notifications for a user"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT n.id, n.from_user_id, n.notification_type, n.message, n.post_id, 
                   n.is_read, n.created_at, u.full_name, u.profile_photo
            FROM notifications n
            LEFT JOIN users u ON n.from_user_id = u.id
            WHERE n.user_id = ?
            ORDER BY n.created_at DESC
        ''', (user_id,))
        notifications = cursor.fetchall()
        conn.close()
        
        return [{
            'id': n[0],
            'from_user_id': n[1],
            'notification_type': n[2],
            'message': n[3],
            'post_id': n[4],
            'is_read': n[5],
            'created_at': n[6],
            'from_user_name': n[7],
            'from_user_photo': n[8]
        } for n in notifications]
    except:
        return []

def get_unread_count(user_id: int) -> int:
    """Get count of unread notifications"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM notifications 
            WHERE user_id = ? AND is_read = 0
        ''', (user_id,))
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except:
        return 0

def mark_as_read(notification_id: int) -> bool:
    """Mark a notification as read"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE notifications SET is_read = 1 WHERE id = ?
        ''', (notification_id,))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def mark_all_as_read(user_id: int) -> bool:
    """Mark all notifications as read"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE notifications SET is_read = 1 WHERE user_id = ?
        ''', (user_id,))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def delete_notification(notification_id: int) -> bool:
    """Delete a notification"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM notifications WHERE id = ?', (notification_id,))
        conn.commit()
        conn.close()
        return True
    except:
        return False