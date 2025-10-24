"""
AI Engine Module
Handles all AI operations using Google Gemini API
Generates explanations, summaries, and quizzes
"""
import google.generativeai as genai
from typing import Dict, List
import json
import re
from config import Config

class AIEngine:
    """AI Engine using Google Gemini for content generation"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize AI Engine with Gemini API
        
        Args:
            api_key: Google Gemini API key
        """
        self.api_key = api_key or Config.GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        
        # Try to initialize with configured model, with fallbacks
        model_names = [
            Config.GEMINI_MODEL,
            "learnlm-2.0-flash-experimental",  # Best for education
            "gemini-2.5-flash",  # Latest stable
            "gemini-flash-latest",  # Always newest
            "gemini-2.0-flash",  # Fallback
        ]
        
        self.model = None
        last_error = None
        
        for model_name in model_names:
            try:
                self.model = genai.GenerativeModel(model_name)
                # Quick test to ensure it works
                test_response = self.model.generate_content("test")
                print(f"✅ Successfully initialized with model: {model_name}")
                break
            except Exception as e:
                last_error = e
                continue
        
        if not self.model:
            raise ValueError(f"Could not initialize any Gemini model. Last error: {last_error}")
    
    def generate_explanation(self, topic: str, learning_level: str, context: str = "") -> str:
        """
        Generate a personalized explanation for a topic
        
        Args:
            topic: The topic to explain
            learning_level: User's learning level (Beginner/Intermediate/Advanced)
            context: Additional context from uploaded files
            
        Returns:
            Detailed explanation as string
        """
        # Build prompt based on learning level
        level_prompts = {
            "Beginner": "Explain this topic in very simple terms, as if teaching a complete beginner. Use everyday examples and avoid jargon.",
            "Intermediate": "Explain this topic with moderate detail, assuming some foundational knowledge. Include relevant examples and concepts.",
            "Advanced": "Provide an in-depth, technical explanation. Include advanced concepts, nuances, and technical terminology."
        }
        
        prompt = f"""
{level_prompts.get(learning_level, level_prompts["Beginner"])}

Topic: {topic}

{f"Additional Context: {context[:2000]}" if context else ""}

Provide a clear, well-structured explanation that is appropriate for a {learning_level} level learner.
Use paragraphs, examples, and make it engaging and easy to understand.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating explanation: {str(e)}"
    
    def generate_summary(self, topic: str, explanation: str, learning_level: str) -> str:
        """
        Generate a concise summary of the topic
        
        Args:
            topic: The topic
            explanation: The full explanation
            learning_level: User's learning level
            
        Returns:
            Concise summary as string
        """
        prompt = f"""
Based on this explanation of {topic}, create a concise summary that captures the key points.

Explanation:
{explanation[:3000]}

Create a summary appropriate for a {learning_level} level learner. 
The summary should:
- Be 3-5 bullet points
- Highlight the most important concepts
- Be easy to remember and review

Format as bullet points using markdown.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def generate_quiz(
        self, 
        topic: str, 
        explanation: str, 
        learning_level: str,
        num_questions: int = 5
    ) -> Dict:
        """
        Generate a practice quiz with multiple choice questions
        
        Args:
            topic: The topic
            explanation: The full explanation
            learning_level: User's learning level
            num_questions: Number of questions to generate
            
        Returns:
            Dictionary containing quiz questions and answers
        """
        prompt = f"""
Based on this explanation of {topic}, create a {num_questions}-question multiple choice quiz.

Explanation:
{explanation[:3000]}

Create questions appropriate for a {learning_level} level learner.

Return the quiz in this EXACT JSON format:
{{
  "questions": [
    {{
      "question": "Question text here?",
      "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
      "correct_answer": "A",
      "explanation": "Brief explanation of why this is correct"
    }}
  ]
}}

Make sure:
- Questions test understanding, not just memorization
- All options are plausible
- Explanations are helpful for learning
- Return valid JSON only, no additional text
"""
        
        try:
            response = self.model.generate_content(prompt)
            quiz_text = response.text
            
            # Extract JSON from response (sometimes wrapped in markdown code blocks)
            json_match = re.search(r'```json\s*(.*?)\s*```', quiz_text, re.DOTALL)
            if json_match:
                quiz_text = json_match.group(1)
            
            # Remove any markdown code block markers
            quiz_text = quiz_text.replace('```json', '').replace('```', '').strip()
            
            # Parse JSON
            quiz_data = json.loads(quiz_text)
            
            # Validate structure
            if "questions" not in quiz_data:
                raise ValueError("Invalid quiz format: missing 'questions' key")
            
            return quiz_data
            
        except json.JSONDecodeError as e:
            # Fallback: create a simple quiz structure
            return {
                "questions": [
                    {
                        "question": f"What is the main concept of {topic}?",
                        "options": [
                            "A) See explanation for details",
                            "B) Review the material above",
                            "C) Check the summary",
                            "D) All of the above"
                        ],
                        "correct_answer": "D",
                        "explanation": "Please review the explanation and summary above."
                    }
                ],
                "error": f"Quiz generation encountered an error: {str(e)}"
            }
        except Exception as e:
            return {
                "questions": [],
                "error": f"Error generating quiz: {str(e)}"
            }
    
    def improve_from_feedback(self, topic: str, feedback: str) -> str:
        """
        Generate improved content based on user feedback
        
        Args:
            topic: The topic
            feedback: User feedback
            
        Returns:
            Suggestions for improvement
        """
        prompt = f"""
A user studied the topic: {topic}
They provided this feedback: {feedback}

Suggest how the explanation or learning materials could be improved based on this feedback.
Be specific and constructive.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error processing feedback: {str(e)}"