# import requirements
import openai
import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from moviepy.editor import *

# load keys
_ = load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")

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
    path = video_path.parent
    fname = video_path.name.replace('mp4', 'mp3')

    # load the mp4 file
    video = VideoFileClip(str(video_path))
    
    # extract audio from video
    audio_path = Path("audio")/fname
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
def get_summary(transcript, number_of_topics, size):
    prompt_zero = f"""
    Your task is to summarize a video transcript delimited by tripple backtics in order to share the main highlights with the company employees.
    - create a {(size+1)*20} word long summary
    
    Only output text in BRAZILIAN PORTUGUESE.

    ```{transcript}```
    """

    prompt = f"""
    Your task is to summarize a video transcript delimited by tripple backtics in order to share the main highlights with the company employees.
    - infer {number_of_topics} topics from the video
    - create a {(size+1)*20} word long summary for each topic
    - Respond using the following structure for each topic:

    #### <Topic>
    <Summary>

    Only output text in BRAZILIAN PORTUGUESE.

    ```{transcript}```
    """
    
    prompt = prompt_zero if number_of_topics == 0 else prompt
    
    summary = get_completion(prompt)
    return summary.replace('$', '\$')

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

# summarize video
def summarize_video(video_path, helper_prompt=""):
    audio_path = video2audio(video_path)
    transcript = get_transcription(audio_path, helper_prompt)
    prompt = f"""
    Your task is to summarize a video transcript delimited by tripple backtics in order to share the main highlights with the company employees.
    - infer at most 3 topics from the video
    - create a 2 sentence summary for each topic
    - Respond using the following structure:

    ## <Topic>
    <Summary>

    Only output text in BRAZILIAN PORTUGUESE.

    ```{transcript}```
    """
    summary = get_completion(prompt)
    return summary
