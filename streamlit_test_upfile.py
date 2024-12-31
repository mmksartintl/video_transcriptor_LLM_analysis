import streamlit as st
from io import StringIO
from pathlib import Path

uploaded_file = st.file_uploader(label="Choose a file", type=["mp4"])
if uploaded_file is not None:
    save_folder = './videorepo'
    video_file = uploaded_file.name
    save_path = Path(save_folder, video_file)
    print(save_path)
    with open(save_path, mode='wb') as w:
       # To read file as bytes:
       bytes_data = uploaded_file.getvalue()
       w.write(bytes_data)

    audio_file = video_file.replace("mp4","m4a")
    st.code(audio_file, wrap_lines=True)
