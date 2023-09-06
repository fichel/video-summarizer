# import requirements
import openai
import streamlit as st
from pathlib import Path
from moviepy.editor import *

# load keys
openai.api_key = st.secrets['OPENAI_API_KEY']

size_to_value = dict([
    ('small', '25 to 50'),
    ('medium', '50 to 100'),
    ('large', '150 to 300')
])

# helper function to get chat completion
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        messages = messages,
        model = model,
        temperature = 0
    )
    return response.choices[0].message.content

# convert mp4 video to mp3 audio
def video2audio(video_path):
    # extract base path and filename
    video_path = Path(video_path)
    fname = video_path.name.replace('mp4', 'mp3')

    # load the mp4 file
    video = VideoFileClip(str(video_path))
    
    # extract audio from video
    audio_dir = Path("audio")
    audio_dir.mkdir(parents=True, exist_ok=True)
    audio_path = audio_dir/fname
    video.audio.write_audiofile(audio_path)
    return audio_path


# helper function to transcribe audio
def get_transcription(audio_path, prompt=""):
    print(f"Transcribing {audio_path}...")
    with open(audio_path, "rb") as audio:
        transcript = openai.Audio.transcribe(
            file = audio,
            model = "whisper-1",
            response_format = "text",
            language = "pt",
            prompt = prompt
        )
    return transcript

# helper function to summarize a video transcript
def get_summary(transcript, number_of_topics, size, language="BRAZILIAN PORTUGUESE"):
    prompt_zero = f"""
    Your task is to summarize a video transcript delimited by tripple backtics in order to share the main highlights with the company employees.
    - create a {size_to_value[size]} word long summary
    
    Only output text in {language}.

    ```{transcript}```
    """

    prompt = f"""
    Your task is to summarize a video transcript delimited by tripple backtics in order to share the main highlights with the company employees.
    - infer exactly {number_of_topics} topics from the video
    - create {size_to_value[size]} word long summaries for each one of the topics
    - avoid duplicating content
    - avoid any final summaries or conclusions at the end. Only summarize each topic
    - Respond using the following structure for each topic:

    #### <Topic>
    <Summary>

    Only output text in {language}.

    ```{transcript}```
    """
    
    prompt = prompt_zero if number_of_topics == 0 else prompt
    
    summary = get_completion(prompt)
    return summary.replace('$', '\$')

# save uploaded video to disk
def save_uploaded_video(video):
    # Create a 'video' directory if it doesn't exist
    video_dir = Path('video')
    video_dir.mkdir(parents=True, exist_ok=True)

    # Save the uploaded video to the 'video' directory
    video_path = video_dir / video.name
    # video_path.write_bytes(video.getbuffer())
    with open(video_path, "wb") as f:
        f.write(video.getbuffer())

    return str(video_path)

# delete all files in a given directory
def delete_files_in_directory(dir_list):
    for directory in dir_list:
        dir_path = Path(directory)
        for file_path in dir_path.glob("*"):
            if file_path.is_file():
                file_path.unlink()
