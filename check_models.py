# Save as check_models.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure with your API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ No API key found!")
    exit()

genai.configure(api_key=api_key)

print("🔍 Checking available models...")
print("=" * 60)

try:
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ Model Name: {model.name}")
            print(f"   Use this in config: {model.name.split('/')[-1]}")
            print()
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nTrying alternative method...")
    
    # Try common model names
    test_models = [
        "gemini-pro",
        "gemini-1.5-flash", 
        "gemini-1.5-pro",
        "gemini-1.5-flash-latest",
        "gemini-pro-latest",
        "models/gemini-pro",
        "models/gemini-1.5-flash"
    ]
    
    for model_name in test_models:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Hello")
            print(f"✅ {model_name} - WORKS!")
        except Exception as e:
            print(f"❌ {model_name} - {str(e)[:50]}...")