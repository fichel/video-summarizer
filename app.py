import streamlit as st
from utils import (
    video2audio, 
    get_transcription, 
    get_summary,
    save_uploaded_video,
    delete_files_in_directory
)

class VideoSummarizer:
    def __init__(self):
        self.transcription = ""
        self.summary = ""
        self.number_of_topics = 3
        self.size = 'medium'

    def extract_audio(self, video):
        # Your code to extract audio
        video_path = save_uploaded_video(video)
        st.session_state.audio_path = video2audio(video_path)

    def extract_transcription(self, audio_path, prompt):
        # Your code to extract transcription
        return get_transcription(audio_path, prompt)

    def summarize_video(self, video_path, number_of_topics, size):
        # Your code to summarize video
        return get_summary(video_path, number_of_topics, size)

SIZE_OPTIONS = ('small', 'medium', 'large')

# remove transcription from session state
def reset_transcription():
    if 'transcription' in st.session_state:
        del st.session_state['transcription']

# clear all session variables and saved files
def clear_cache():
    if 'audio_path' in st.session_state:
        del st.session_state['audio_path']
    if 'transcription' in st.session_state:
        del st.session_state['transcription']
    # delete media files
    delete_files_in_directory(['video', 'audio'])

def main():
    st.title("📺 Video Summarizer")

    st.sidebar.header("Controls")
    st.sidebar.slider("Number of topics", 0, 5, 3, key="number_of_topics")
    st.sidebar.radio("Choose the size of the summary", SIZE_OPTIONS, index=1, key="size")
    st.sidebar.text_input("Helper prompt", key="prompt", on_change=reset_transcription)
    video = st.file_uploader("Upload a video", 
                     type=['mp4', 'avi', 'mov', 'flv', 'wmv'], 
                     key="uploaded_file", 
                     accept_multiple_files=False,
                     on_change=clear_cache
    )

    # display video
    if video:
        st.video(video)

    if st.session_state.uploaded_file is not None:
        video_summarizer = VideoSummarizer()
        if st.button('Summarize Video'):
            if "audio_path" not in st.session_state:
                with st.spinner("Extracting audio..."):
                    video_summarizer.extract_audio(st.session_state.uploaded_file)
                st.success('Finished audio extraction.', icon='✅')
            else: 
                st.info('Using cached audio extraction.', icon='ℹ️')
            if "transcription" not in st.session_state:                    
                with st.spinner("Transcribing audio..."):
                    st.session_state.transcription = video_summarizer.extract_transcription(
                        st.session_state.audio_path, 
                        st.session_state.prompt
                    )
                st.success('Finished audio transcription.', icon='✅')
                # st.header('Transcription')
                # st.session_state.trancription = st.text_area('', st.session_state.transcription, height=300)
            else: 
                st.info('Using cached transcription.', icon='ℹ️')
                # st.session_state.trancription = st.text_area('', st.session_state.transcription, height=300)

            with st.spinner("Summarizing..."):
                summary = video_summarizer.summarize_video(
                    st.session_state.transcription, 
                    st.session_state.number_of_topics, 
                    st.session_state.size
                )
            st.success('Finished summarization.', icon='✅')
            st.divider()
            st.header('Video Summary')
            st.markdown(summary, unsafe_allow_html=False)
            st.write(f"Words: {len(summary.split())}")
            st.balloons()
        
if __name__ == "__main__":
    main()
