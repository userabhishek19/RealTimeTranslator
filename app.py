import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import speech_recognition as sr
from googletrans import Translator
import pyttsx3
from gtts import gTTS
import os
from io import BytesIO
from pydub import AudioSegment
import uuid
import tempfile

st.set_page_config(page_title="Real-time Voice Translator", layout="centered")
st.title("🌍 Real-Time Voice & Video Translator")

# Language selection
languages = {
    'English': 'en', 'Hindi': 'hi', 'French': 'fr', 'Spanish': 'es',
    'German': 'de', 'Chinese': 'zh-cn', 'Arabic': 'ar', 'Bengali': 'bn',
    'Japanese': 'ja', 'Russian': 'ru', 'Urdu': 'ur'
}

col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("You Speak (From)", list(languages.keys()), index=0)
with col2:
    target_lang = st.selectbox("They Hear (To)", list(languages.keys()), index=1)

room_id = st.text_input("Room ID (share with other participant)", "test-room")

# Google Translator
translator = Translator()

def audio_to_text(audio_file):
    recognizer = sr.Recognizer()
    temp_input_path = f"temp_input_{uuid.uuid4().hex}.wav"
    audio = AudioSegment.from_file(audio_file)
    audio.export(temp_input_path, format="wav")

    try:
        with sr.AudioFile(temp_input_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language=languages[source_lang])
    except sr.UnknownValueError:
        text = "Sorry, could not understand audio."
    except sr.RequestError as e:
        text = f"API Error: {e}"
    finally:
        os.remove(temp_input_path)

    return text

def translate_text(text):
    translated = translator.translate(text, src=languages[source_lang], dest=languages[target_lang])
    return translated.text

def text_to_speech(text, lang):
    tts = gTTS(text=text, lang=lang)
    temp_path = os.path.join(tempfile.gettempdir(), f"speech_{uuid.uuid4().hex}.mp3")
    tts.save(temp_path)
    return temp_path

st.markdown("### Record your voice message")
audio_data = st.file_uploader("Record your voice (real-time support depends on browser)", type=["mp3", "wav", "m4a"])

if audio_data is not None:
    st.audio(audio_data, format='audio/wav')
    original_text = audio_to_text(audio_data)
    st.markdown(f"**You said:** {original_text}")

    translated_text = translate_text(original_text)
    st.markdown(f"**Translated:** {translated_text}")

    audio_path = text_to_speech(translated_text, languages[target_lang])
    st.audio(audio_path)

st.markdown("---")
st.subheader("🚀 Start Video & Audio Room")

def app_video():
    webrtc_streamer(
        key="video-room",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"video": True, "audio": True},
        async_processing=True
    )

app_video()
