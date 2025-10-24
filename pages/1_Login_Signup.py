import streamlit as st
import sys
import os

# Fix path to import backend
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.database import Database
from config import Config

# ✅ Initialize database in session state
if 'db' not in st.session_state:
    st.session_state.db = Database()

# Initialize login state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None


st.markdown("## 👤 Account")

if not st.session_state.logged_in:
    login_tab, signup_tab = st.tabs(["🔑 Login", "🆕 Signup"])

    with login_tab:
        login_username = st.text_input("Username")
        login_password = st.text_input("Password", type="password")
        if st.button("Login"):
            user_id = st.session_state.db.authenticate_user(login_username, login_password)
            if user_id:
                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.session_state.username = login_username
                st.success(f"Welcome back, {login_username}! 🎓")
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with signup_tab:
        new_username = st.text_input("Choose a Username")
        new_password = st.text_input("Create Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        learning_level = st.selectbox("Learning Level", Config.LEARNING_LEVELS)

        if st.button("Create Account"):
            if new_password == confirm_password:
                success = st.session_state.db.create_user_account(new_username, new_password, learning_level)
                if success:
                    st.success("🎉 Account created successfully! Please log in.")
                else:
                    st.error("Username already exists.")
            else:
                st.warning("Passwords do not match.")
else:
    st.success(f"Logged in as **{st.session_state.username}**")
    if st.button("Logout", type="secondary"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.current_session = None
        st.session_state.show_quiz_results = False
        st.experimental_rerun()

    # Optional: Add a redirect button to Main App
    if st.button("Go to Study Dashboard"):
        st.switch_page("pages/2_Main_App.py")