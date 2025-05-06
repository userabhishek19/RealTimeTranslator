from gtts import gTTS
from playsound import playsound
import os
import tempfile

def speak_text(text, lang='en'):
    try:
        tts = gTTS(text=text, lang=lang)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            playsound(fp.name)
            os.remove(fp.name)
    except Exception as e:
        print(f"Error speaking text: {str(e)}")
