from langchain_groq import ChatGroq

llm = ChatGroq(temperature=0,groq_api_key='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',
               model_name="llama3-8b-8192")

import subprocess

def convert_video_to_audio(video_path, audio_path):
    """Convert video file to audio file using ffmpeg"""
    command = [
        "ffmpeg",
        "-i", video_path,
        "-ar", "16000",  # Set sample rate to 16000 Hz
        "-ac", "1",      # Set to mono
        "-f", "wav",     # Output format
        "-y", "-v", "quiet",
        audio_path
    ]
    subprocess.run(command, check=True)

import os
from groq import Groq

# Initialize the Groq client
client = Groq(api_key='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')

def convert_audio_to_transcript(filename):

    # Open the audio file
    with open(filename, "rb") as file:
        # Create a translation of the audio file
        translation = client.audio.translations.create(
            file=(filename, file.read()), # Required audio file
            model="whisper-large-v3", # Required model to use for translation
            prompt="Specify context or spelling",  # Optional
            response_format="json",  # Optional
            temperature=0.0  # Optional
        )
    # Print the translation text
    return(translation.text)

from langchain_core.prompts import PromptTemplate

prompt_extract = PromptTemplate.from_template(
    """
    ### SCRAPED TEXT FROM WEBSITE:
    {page_data}
    ### INSTRUCTION:
    {instructions_data}
    ### NO JSON OUTPUT AND NO PREAMBLE
    """
)

chain_extract = prompt_extract | llm

#res = chain_extract.invoke(input={'page_data': translation.text})
#print(res.content)

import streamlit as st
from io import StringIO
from pathlib import Path

uploaded_file = st.file_uploader(label="Choose a file", type=["mp4"])

if uploaded_file is not None:

    save_folder = './videorepo'
    video_file = uploaded_file.name
    save_path = Path(save_folder, video_file)

    with open(save_path, mode='wb') as w:
       # To read file as bytes:
       bytes_data = uploaded_file.getvalue()
       w.write(bytes_data)

    video_file = str(save_path.resolve())
    audio_file = video_file.replace("mp4","m4a")
    convert_video_to_audio(video_file, audio_file)

prompt_question = st.text_area("Enter instructions :")
submit_button = st.button("Submit")

if submit_button:

    transcript = convert_audio_to_transcript(audio_file)

    res = chain_extract.invoke(input={'page_data': transcript, 'instructions_data': prompt_question})

    st.code(res.content, wrap_lines=True)

    st.session_state.llm_content = res.content 
