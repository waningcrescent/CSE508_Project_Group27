import os
import google.generativeai as genai

def chatbot_response(user_text):
    api_key = os.environ.get("GOOGLE_API_KEY", "YOUR_GOOGLE_API_KEY_HERE")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(user_text)
    return response.text

print(chatbot_response("Does whatsapp use my camera?"))
