import os
import dotenv
import openai
import streamlit as st
from googletrans import Translator

# import API key from .env file
dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


#speech to text
def transcribe(input_file):
    transcript = openai.Audio.transcribe("whisper-1", input_file) #dictionary
    return transcript


# save file upload
def save_file(audio_bytes, file_name):
    with open(file_name, "wb") as f:
        f.write(audio_bytes)


# read  file upload and transcribe
def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        transcript = transcribe(audio_file)

    return transcript["text"]


#change language
def translate_text(text, language_desire):
    translator = Translator()
    translated_text = translator.translate(text, dest=language_desire)
    return translated_text.text



def transcribe_and_translate(input_file, language_desire):
    #get name_file_input and remove extend
    name_file_input = os.path.splitext(input_file.name)[0]

    # render type input_file /mp4
    audio_file_name = f"{name_file_input}.{input_file.type.split('/')[1]}" #

    #create .txt
    transcript_file_name = f"{name_file_input}_transcript.txt"

    #save file
    save_file(input_file.read(), audio_file_name)

    #contains text of audio_file_name
    transcript_text = transcribe_audio(audio_file_name)

    st.header("Language Of The File")
    st.write(transcript_text)

    #input .txt
    with open(transcript_file_name, "w") as f:
        f.write(transcript_text)


    if language_desire.lower() != input_file.type.split('-')[0].lower():
        # Translate only if the selected language is different from the input language
        translated_text = translate_text(transcript_text, language_desire)
        translated_file_name = f"{name_file_input}_transcript_{language_desire}.txt"

        with open(translated_file_name, "w") as f:
            f.write(translated_text)

        st.header(f"Translation For File Language ({language_desire})")
        st.write(translated_text)
        st.download_button(f"Download Translation For File Language ({language_desire})", translated_text,
                           file_name=translated_file_name)

    st.download_button("Download Language Of The File", transcript_text, file_name=transcript_file_name)


def main():
    st.title("SPEECH TO TEXT")

    target_language = st.selectbox("Select language to translate", ["en", "fr", "es"])

    audio_file = st.file_uploader("Upload file", type=["mp3", "mp4", "wav", "m4a"])

    if audio_file:
        if st.button("Create Language Of The File and Translation For File Language"):
            transcribe_and_translate(audio_file, target_language)


if __name__ == "__main__":
    main()
