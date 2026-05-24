import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GEMINI_API_KEY")
print("Key length:", len(key) if key else 0)

try:
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content("Write a one sentence joke about finance.")
    print("SUCCESS:")
    print(response.text)
except Exception as e:
    print("ERROR:")
    print(str(e))
