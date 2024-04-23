import google.generativeai as genai

def chatbot_response(user_text):
    api_key='AIzaSyBZrc45HezRry5aOhR7XKHAOn20x6TVeBE'
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(user_text)
    return response.text