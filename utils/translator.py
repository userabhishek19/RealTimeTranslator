from deep_translator import GoogleTranslator

def translate_text(text, src='en', dest='hi'):
    try:
        translated = GoogleTranslator(source=src, target=dest).translate(text)
        return translated
    except Exception as e:
        return f"Translation error: {str(e)}"
