from deep_translator import GoogleTranslator

def translate_text(text, target='en'):
    translator = GoogleTranslator(source='auto', target=target)
    return translator.translate(text)