import streamlit as st
import sys
import os

# Add the root directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.ai_engine import AIEngine
from backend.content_processor import ContentProcessor
from backend.database import Database
from config import Config

# Page configuration
st.set_page_config(
    page_title="EduGenie - AI Study Assistant",
    page_icon="🧞‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 0;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1E88E5;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .quiz-question {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state components
if 'ai_engine' not in st.session_state:
    st.session_state.ai_engine = None
if 'db' not in st.session_state:
    st.session_state.db = Database()
if 'current_session' not in st.session_state:
    st.session_state.current_session = None
if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = {}
if 'show_quiz_results' not in st.session_state:
    st.session_state.show_quiz_results = False

def initialize_ai_engine(api_key: str):
    """Initialize AI Engine with API key"""
    try:
        st.session_state.ai_engine = AIEngine(api_key)
        return True
    except Exception as e:
        st.error(f"Error initializing AI Engine: {str(e)}")
        return False

def process_topic(topic: str, learning_level: str, file_content: str = ""):
    """Process a topic and generate all content"""
    with st.spinner("🧞‍♂️ EduGenie is working its magic..."):
        # Generate explanation
        explanation = st.session_state.ai_engine.generate_explanation(
            topic, learning_level, file_content
        )
        
        # Generate summary
        summary = st.session_state.ai_engine.generate_summary(
            topic, explanation, learning_level
        )
        
        # Generate quiz
        quiz_data = st.session_state.ai_engine.generate_quiz(
            topic, explanation, learning_level
        )
        
        # Save to session state
        st.session_state.current_session = {
            'topic': topic,
            'learning_level': learning_level,
            'explanation': explanation,
            'summary': summary,
            'quiz_data': quiz_data
        }
        
        # Save to database if user exists
        if 'user_id' in st.session_state:
            session_id = st.session_state.db.save_session(
                st.session_state.user_id,
                topic,
                learning_level,
                explanation,
                summary,
                quiz_data
            )
            st.session_state.current_session['session_id'] = session_id

def display_quiz():
    """Display quiz questions and handle answers"""
    quiz_data = st.session_state.current_session['quiz_data']
    
    if 'error' in quiz_data:
        st.warning(quiz_data['error'])
        return
    
    questions = quiz_data.get('questions', [])
    
    if not questions:
        st.warning("No quiz questions available.")
        return
    
    st.markdown('<p class="section-header">📝 Practice Quiz</p>', unsafe_allow_html=True)
    
    for i, q in enumerate(questions):
        st.markdown(f'<div class="quiz-question">', unsafe_allow_html=True)
        st.markdown(f"**Question {i+1}:** {q['question']}")
        
        # Radio buttons for options
        answer = st.radio(
            f"Select your answer for Question {i+1}:",
            q['options'],
            key=f"q_{i}",
            label_visibility="collapsed"
        )
        
        if answer:
            st.session_state.quiz_answers[i] = answer[0]  # Store just the letter (A, B, C, D)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Submit quiz button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Submit Quiz", type="primary"):
            st.session_state.show_quiz_results = True
    
    # Show results if submitted
    if st.session_state.show_quiz_results:
        st.markdown("---")
        st.markdown("### 🎯 Quiz Results")
        
        correct_count = 0
        for i, q in enumerate(questions):
            user_answer = st.session_state.quiz_answers.get(i, "")
            correct_answer = q['correct_answer']
            
            if user_answer == correct_answer:
                st.success(f"✅ Question {i+1}: Correct!")
                correct_count += 1
            else:
                st.error(f"❌ Question {i+1}: Incorrect. Correct answer: {correct_answer}")
            
            with st.expander(f"Explanation for Question {i+1}"):
                st.write(q['explanation'])
        
        score = (correct_count / len(questions)) * 100
        st.markdown(f"### Final Score: {score:.1f}% ({correct_count}/{len(questions)})")
        
        if score >= 80:
            st.balloons()
            st.success("🎉 Excellent work! You've mastered this topic!")
        elif score >= 60:
            st.info("👍 Good job! Review the explanations and try again to improve.")
        else:
            st.warning("📚 Keep studying! Review the material and try again.")

# Header
st.markdown('<p class="main-header">🧞‍♂️ EduGenie</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Your AI-Powered Personalized Study Assistant</p>', unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    
    # API Key input
    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        value=Config.GEMINI_API_KEY,
        help="Get your API key from https://makersuite.google.com/app/apikey  "
    )
    
    if api_key and not st.session_state.ai_engine:
        if initialize_ai_engine(api_key):
            st.success("✅ AI Engine initialized!")
    
    st.markdown("---")

# Main content area
if not st.session_state.ai_engine:
    st.warning("⚠️ Please enter your Gemini API Key in the sidebar to get started.")
    st.info("""
    **How to get your API Key:**
    1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey  )
    2. Sign in with your Google account
    3. Click "Create API Key"
    4. Copy and paste it in the sidebar
    """)
    st.stop()

# Input section
st.markdown("## 🎯 What would you like to learn today?")

col1, col2 = st.columns([3, 1])

with col1:
    topic = st.text_input(
        "Enter a topic or question",
        placeholder="e.g., Photosynthesis, Quantum Computing, Python Functions..."
    )

with col2:
    learning_level = st.selectbox(
        "Learning Level",
        Config.LEARNING_LEVELS,
        index=0
    )

# File upload section
st.markdown("### 📎 Upload Study Material (Optional)")
uploaded_file = st.file_uploader(
    "Upload PDF, TXT, or DOCX file",
    type=['pdf', 'txt', 'docx'],
    help="Upload additional study materials to provide context"
)

file_content = ""
if uploaded_file:
    try:
        file_bytes = uploaded_file.read()
        file_content = ContentProcessor.process_file(file_bytes, uploaded_file.name)
        
        # Truncate if too long
        file_content = ContentProcessor.truncate_text(file_content, max_length=5000)
        
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        with st.expander("Preview extracted text"):
            st.text(file_content[:500] + "..." if len(file_content) > 500 else file_content)
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")

# Generate button
if st.button("✨ Generate Study Materials", type="primary", disabled=not topic):
    if topic:
        process_topic(topic, learning_level, file_content)
        st.session_state.show_quiz_results = False
        st.session_state.quiz_answers = {}

# Display results if available
if st.session_state.current_session:
    session = st.session_state.current_session
    
    st.markdown("---")
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["📖 Explanation", "📋 Summary", "📝 Quiz", "💬 Feedback"])
    
    with tab1:
        st.markdown('<p class="section-header">📖 Detailed Explanation</p>', unsafe_allow_html=True)
        st.markdown(f"**Topic:** {session['topic']}")
        st.markdown(f"**Level:** {session['learning_level']}")
        st.markdown("---")
        st.markdown(session['explanation'])
    
    with tab2:
        st.markdown('<p class="section-header">📋 Key Points Summary</p>', unsafe_allow_html=True)
        st.markdown(session['summary'])
        
        # Download summary button
        st.download_button(
            label="📥 Download Summary",
            data=f"# {session['topic']}\n\n{session['summary']}",
            file_name=f"{session['topic'].replace(' ', '_')}_summary.md",
            mime="text/markdown"
        )
    
    with tab3:
        display_quiz()
    
    with tab4:
        st.markdown('<p class="section-header">💬 Provide Feedback</p>', unsafe_allow_html=True)
        st.write("Help us improve your learning experience!")
        
        rating = st.slider("How helpful was this session?", 1, 5, 3)
        feedback_text = st.text_area(
            "Additional comments (optional)",
            placeholder="What did you like? What could be improved?"
        )
        
        if st.button("Submit Feedback"):
            if 'session_id' in session:
                st.session_state.db.save_feedback(
                    session['session_id'],
                    rating,
                    feedback_text
                )
                st.success("Thank you for your feedback! 🙏")
            else:
                st.info("Feedback saved locally. Sign in to save to your profile.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>Built with ❤️ using Streamlit and Google Gemini AI</p>
    <p>🧞‍♂️ EduGenie - Making Learning Personal and Fun</p>
</div>
""", unsafe_allow_html=True)

# Navigation to Dashboard if logged in
if 'logged_in' in st.session_state and st.session_state.logged_in:
    if st.button("Go to Dashboard"):
        st.switch_page("pages/3_Dashboard.py")