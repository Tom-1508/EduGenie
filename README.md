# 🧞‍♂️ EduGenie - AI-Powered Personalized Study Assistant

EduGenie is a comprehensive AI-powered study assistant that simplifies complex topics, generates summaries, and creates personalized quizzes tailored to your learning level.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red.svg)
![Gemini](https://img.shields.io/badge/Gemini-API-green.svg)

## ✨ Features

### Core Functionality
- **📖 Personalized Explanations**: Get topic explanations tailored to your learning level (Beginner/Intermediate/Advanced)
- **📋 Smart Summaries**: AI-generated summaries that highlight key concepts
- **📝 Interactive Quizzes**: Practice with auto-generated multiple-choice questions
- **📎 File Upload Support**: Upload PDF, TXT, or DOCX files for additional context
- **💾 Progress Tracking**: Save your study sessions and track learning history
- **💬 Feedback System**: Rate sessions and provide feedback for improvement

### Technical Features
- Clean, intuitive web interface built with Streamlit
- Google Gemini AI integration for high-quality content generation
- SQLite database for persistent storage
- Modular architecture for easy maintenance and extension

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key ([Get it here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone or download the project**
```bash
# If using git
git clone <your-repo-url>
cd edugenie

# Or download and extract the ZIP file
```

2. **Create a virtual environment (recommended)**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_actual_api_key_here
```

Alternatively, you can enter your API key directly in the web interface.

### Running the Application

**Local Development:**
```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

## 📁 Project Structure

```
edugenie/
├── app.py                      # Main Streamlit application
├── config.py                   # Configuration and settings
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # This file
├── backend/
│   ├── __init__.py           # Package initialization
│   ├── ai_engine.py          # Gemini AI integration
│   ├── content_processor.py  # File processing utilities
│   └── database.py           # SQLite database operations
└── edugenie.db               # SQLite database (created on first run)
```

## 🎯 How to Use

1. **Enter Your API Key**
   - Open the sidebar
   - Paste your Gemini API key
   - The AI engine will initialize automatically

2. **Create a User Profile (Optional)**
   - Enter a username in the sidebar
   - Track your progress and history

3. **Start Learning**
   - Enter a topic in the main input field
   - Select your learning level
   - Optionally upload study materials (PDF/TXT/DOCX)
   - Click "Generate Study Materials"

4. **Explore Content**
   - **Explanation Tab**: Read detailed explanation
   - **Summary Tab**: Review key points and download
   - **Quiz Tab**: Test your knowledge
   - **Feedback Tab**: Rate the session

5. **Review History**
   - Access previous topics from the sidebar
   - Track your learning progress

## 🔧 Configuration

Edit `config.py` to customize:
- Maximum file upload size
- Number of quiz questions
- Database path
- AI model settings

## 🌐 Deployment Options

### Streamlit Cloud (Recommended for MVP)
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add `GEMINI_API_KEY` to secrets
5. Deploy!

### Heroku
```bash
# Install Heroku CLI, then:
heroku create your-edugenie-app
git push heroku main
heroku config:set GEMINI_API_KEY=your_key
```

### Local Network Access
```bash
streamlit run app.py --server.address 0.0.0.0
```

## 🛠️ Development

### Adding New Features

**Add a new AI capability:**
1. Edit `backend/ai_engine.py`
2. Add new method to `AIEngine` class
3. Call from `app.py`

**Add new file format support:**
1. Edit `backend/content_processor.py`
2. Add extraction method
3. Update `process_file()` method

**Modify database schema:**
1. Edit `backend/database.py`
2. Add migration logic in `init_database()`

### Testing

```bash
# Test individual modules
python -c "from backend.ai_engine import AIEngine; print('AI Engine OK')"
python -c "from backend.database import Database; print('Database OK')"
python -c "from backend.content_processor import ContentProcessor; print('Processor OK')"
```

## 📊 Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `learning_level`: Default learning level
- `created_at`: Timestamp

### Study Sessions Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `topic`: Topic studied
- `learning_level`: Level used
- `explanation`, `summary`, `quiz_data`: Generated content
- `created_at`: Timestamp

### Feedback Table
- `id`: Primary key
- `session_id`: Foreign key to study_sessions
- `rating`: 1-5 rating
- `comment`: Optional feedback text
- `created_at`: Timestamp

## 🔒 API Key Security

**Important**: Never commit your `.env` file or expose API keys in code!

- Use `.env` file for local development (already in `.gitignore`)
- Use environment variables for production
- Use Streamlit secrets for Streamlit Cloud deployment

## 🐛 Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "Invalid API key" error
- Verify your Gemini API key is correct
- Check that key is properly set in `.env` or sidebar
- Ensure you have API quota available

### File upload fails
- Check file size (default max: 10MB)
- Ensure file format is PDF, TXT, or DOCX
- Try a different file

### Database errors
- Delete `edugenie.db` to reset database
- Check file permissions in project directory

## 📝 License

This project is created for educational and hackathon purposes.

## 🤝 Contributing

This is a hackathon MVP. Feel free to fork and enhance!

### Ideas for Enhancement
- Add more file formats (images with OCR)
- Implement spaced repetition system
- Add collaborative study groups
- Export to Anki/Quizlet
- Voice input/output
- Multi-language support
- Integration with note-taking apps

## 📧 Support

For issues or questions:
1. Check this README
2. Review code comments
3. Check Gemini API documentation
4. Check Streamlit documentation

## 🎉 Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- Powered by [Google Gemini](https://deepmind.google/technologies/gemini/)
- Created for hackathon participants worldwide

---

**Happy Learning with EduGenie! 🧞‍♂️✨**