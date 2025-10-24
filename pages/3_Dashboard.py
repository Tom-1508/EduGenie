import streamlit as st
import sys
import os

# Add the root directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.database import Database

st.markdown("## 📊 Your Learning Dashboard")

if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("🔒 Please log in first to view your dashboard.")
    if st.button("Go to Login"):
        st.switch_page("pages/1_Login_Signup.py")
    st.stop()

# User stats
st.success(f"Logged in as **{st.session_state.username}**")

if st.session_state.user_id:
    stats = st.session_state.db.get_user_stats(st.session_state.user_id)
    st.metric("Total Sessions", stats['total_sessions'])
    st.metric("Topics Studied", stats['unique_topics'])

# User history
st.markdown("## 📚 Recent Topics")
history = st.session_state.db.get_user_history(st.session_state.user_id, limit=5)

if history:
    for item in history:
        if st.button(f"📖 {item['topic'][:30]}...", key=f"hist_{item['id']}"):
            session = st.session_state.db.get_session(item['id'])
            if session:
                st.session_state.current_session = {
                    'topic': session['topic'],
                    'learning_level': session['learning_level'],
                    'explanation': session['explanation'],
                    'summary': session['summary'],
                    'quiz_data': session['quiz_data'],
                    'session_id': session['id']
                }
                st.switch_page("pages/2_Main_App.py")

# Optional: Back to main app
if st.button("Back to Study App"):
    st.switch_page("pages/2_Main_App.py")