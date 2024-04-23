import google.generativeai as genai

def chatbot_response(user_text):
    api_key="AIzaSyCrkcA_n7wp100fxfgrUwYK_jCIMLEt9jk"
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(user_text)
    return response.text

print(chatbot_response("Does whatsapp use my camera?"))
