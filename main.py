
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

convert_video_to_audio("videorepo/AI_Is_Dangerous.mp4", "videorepo/AI_Is_Dangerous.m4a")

import os
from groq import Groq

# Initialize the Groq client
client = Groq(api_key='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')

# Specify the path to the audio file
filename = "videorepo/AI_Is_Dangerous.m4a" # Replace with your audio file!

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
    #print(translation.text)	

from langchain_core.prompts import PromptTemplate

prompt_extract = PromptTemplate.from_template(
    """
    ### SCRAPED TEXT FROM WEBSITE:
    {page_data}
    ### INSTRUCTION:
    Scraped text is from an interview.
    Create briefing about this interview highlighting important topics.
    Please translate in Portuguese.
    ### VALID JSON (NO PREAMBLE)
    """
)

chain_extract = prompt_extract | llm

res = chain_extract.invoke(input={'page_data': translation.text})
print(res.content)
