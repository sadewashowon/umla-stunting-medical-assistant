import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import sqlite3
import os
import hashlib
import secrets

def init_auth_db():
    """Initialize the authentication database"""
    conn = sqlite3.connect('stunting_assistant.db')
    cursor = conn.cursor()
    
    # Create users table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed_password):
    """Verify a password against its hash"""
    return hash_password(password) == hashed_password

def register_user(username, password, email, name):
    """Register a new user"""
    try:
        conn = sqlite3.connect('stunting_assistant.db')
        cursor = conn.cursor()
        
        # Check if username already exists
        cursor.execute('SELECT username FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            return False, "Username already exists"
        
        # Hash password and insert user
        hashed_password = hash_password(password)
        cursor.execute('''
            INSERT INTO users (username, password, email, name)
            VALUES (?, ?, ?, ?)
        ''', (username, hashed_password, email, name))
        
        conn.commit()
        conn.close()
        return True, "User registered successfully"
    
    except Exception as e:
        return False, f"Registration failed: {str(e)}"

def authenticate_user(username, password):
    """Authenticate a user"""
    try:
        conn = sqlite3.connect('stunting_assistant.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT password, name FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        
        if result and verify_password(password, result[0]):
            return True, result[1]  # Return success and name
        else:
            return False, "Invalid username or password"
    
    except Exception as e:
        return False, f"Authentication failed: {str(e)}"

def get_user_info(username):
    """Get user information"""
    try:
        conn = sqlite3.connect('stunting_assistant.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT username, email, name, created_at FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        
        if result:
            return {
                'username': result[0],
                'email': result[1],
                'name': result[2],
                'created_at': result[3]
            }
        return None
    
    except Exception as e:
        return None

def update_user_profile(username, email=None, name=None):
    """Update user profile information"""
    try:
        conn = sqlite3.connect('stunting_assistant.db')
        cursor = conn.cursor()
        
        if email and name:
            cursor.execute('''
                UPDATE users SET email = ?, name = ? WHERE username = ?
            ''', (email, name, username))
        elif email:
            cursor.execute('UPDATE users SET email = ? WHERE username = ?', (email, username))
        elif name:
            cursor.execute('UPDATE users SET name = ? WHERE username = ?', (name, username))
        
        conn.commit()
        conn.close()
        return True, "Profile updated successfully"
    
    except Exception as e:
        return False, f"Profile update failed: {str(e)}"

def change_password(username, old_password, new_password):
    """Change user password"""
    try:
        # First verify old password
        success, message = authenticate_user(username, old_password)
        if not success:
            return False, "Current password is incorrect"
        
        # Update to new password
        conn = sqlite3.connect('stunting_assistant.db')
        cursor = conn.cursor()
        
        new_hashed_password = hash_password(new_password)
        cursor.execute('UPDATE users SET password = ? WHERE username = ?', (new_hashed_password, username))
        
        conn.commit()
        conn.close()
        return True, "Password changed successfully"
    
    except Exception as e:
        return False, f"Password change failed: {str(e)}"

def delete_user(username, password):
    """Delete a user account"""
    try:
        # First verify password
        success, message = authenticate_user(username, password)
        if not success:
            return False, "Password is incorrect"
        
        # Delete user and their chat history
        conn = sqlite3.connect('stunting_assistant.db')
        cursor = conn.cursor()
        
        # Delete chat history first (due to foreign key constraint)
        cursor.execute('DELETE FROM chat_history WHERE username = ?', (username,))
        
        # Delete user
        cursor.execute('DELETE FROM users WHERE username = ?', (username,))
        
        conn.commit()
        conn.close()
        return True, "Account deleted successfully"
    
    except Exception as e:
        return False, f"Account deletion failed: {str(e)}"

def get_all_users():
    """Get all users (admin function)"""
    try:
        conn = sqlite3.connect('stunting_assistant.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT username, email, name, created_at FROM users ORDER BY created_at DESC')
        users = cursor.fetchall()
        
        conn.close()
        return users
    
    except Exception as e:
        return []

def create_demo_user():
    """Create a demo user if no users exist"""
    try:
        conn = sqlite3.connect('stunting_assistant.db')
        cursor = conn.cursor()
        
        # Check if any users exist
        cursor.execute('SELECT COUNT(*) FROM users')
        user_count = cursor.fetchone()[0]
        
        if user_count == 0:
            # Create demo user
            demo_password = hash_password('demo123')
            cursor.execute('''
                INSERT INTO users (username, password, email, name)
                VALUES (?, ?, ?, ?)
            ''', ('demo', demo_password, 'demo@example.com', 'Demo User'))
            
            conn.commit()
            conn.close()
            return True, "Demo user created"
        
        conn.close()
        return False, "Users already exist"
    
    except Exception as e:
        return False, f"Demo user creation failed: {str(e)}"
