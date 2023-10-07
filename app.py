import streamlit as st
from utils import (
    video2audio, 
    get_transcription, 
    get_summary,
    save_uploaded_video,
    delete_files_in_directory
)
from typing import List

class VideoSummarizer:
    def __init__(self):
        self.transcription = ""
        self.summary = ""
        self.number_of_topics = 3
        self.size = 'medium'

    def extract_audio(self, video):
        video_path = save_uploaded_video(video)
        st.session_state.audio_path = video2audio(video_path)

    def extract_transcription(self, audio_path, prompt):
        return get_transcription(audio_path, prompt)

    def summarize_video(self, transcription, number_of_topics, size):
        return get_summary(transcription, number_of_topics, size)

class MultiVideoSummarizer:
    def __init__(self):
        self.summarizers = []

    def add_summarizer(self, summarizer: VideoSummarizer):
        self.summarizers.append(summarizer)

    def process_and_summarize(self, videos: List):
        summaries = []
        for video in videos:
            summarizer = VideoSummarizer()
            summarizer.extract_audio(video)
            transcription = summarizer.extract_transcription(
                st.session_state.audio_path,
                st.session_state.prompt
            )
            summary = summarizer.summarize_video(
                transcription,
                st.session_state.number_of_topics,
                st.session_state.size
            )
            summaries.append((video.name, summary))
        return summaries

SIZE_OPTIONS = ('small', 'medium', 'large')

def reset_transcription():
    if 'transcription' in st.session_state:
        del st.session_state['transcription']

def clear_cache():
    if 'audio_path' in st.session_state:
        del st.session_state['audio_path']
    if 'transcription' in st.session_state:
        del st.session_state['transcription']
    delete_files_in_directory(['video', 'audio'])

def main():
    st.title("📺 Multi Video Summarizer")

    st.sidebar.header("Controls")
    st.sidebar.slider("Number of topics", 0, 5, 3, key="number_of_topics")
    st.sidebar.radio("Choose the size of the summary", SIZE_OPTIONS, index=1, key="size")
    st.sidebar.text_input("Helper prompt", key="prompt", on_change=reset_transcription)
    
    videos = st.file_uploader(
        "Upload videos", 
        type=['mp4'], 
        accept_multiple_files=True,
        on_change=clear_cache
    )

    if videos:
        for video in videos:
            st.video(video)

    if videos is not None:
        multi_summarizer = MultiVideoSummarizer()
        if st.button('Summarize Videos'):
            with st.spinner("Processing and Summarizing Videos..."):
                summaries = multi_summarizer.process_and_summarize(videos)
                st.success('Finished processing and summarizing videos.')
            for video_name, summary in summaries:
                st.divider()
                st.header(f'Video Summary for {video_name}')
                st.markdown(summary, unsafe_allow_html=False)
                st.write(f"Words: {len(summary.split())}")
            st.balloons()

if __name__ == "__main__":
    main()
