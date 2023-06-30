# 📺 video-summarizer
Video Summarizer App that infers topics

The summarizarion works as follows:

1. User uploads a video (currently supports mp4 only)
2. Extract the audio and save it as mp3 by using moviepy (ffmpeg under the hood)
3. Extract the transcription from the mp3 using OpenAI's Audio transcription (Whisper) API 
4. Infer topics and summarize transcriptionusing OpenAI's Chatcompletion API 

## Prerequisites

- Python 3.9 or higher
- Operating System: macOS or Linux

## Steps to Run the Chat UI

1. Fork this repository or create a code space in GitHub.

2. Install the required Python packages by running the following command in your terminal:
   ```
   pip install -r requirements.txt
   ```

3. Install ffmpeg
   * If you're on mac:
   ```
   brew install ffmpeg
   ```
   * On linux:
   ```
   sudo apt-get install ffmpeg
   ```

4. Create a `secrets.toml` file in the `.streamlit` directory. You can use the `secrets_example.toml` file as a reference. Add your OpenAI API Key to the `secrets.toml` file in the following format:
   ```
   OPENAI_API_KEY=your_openai_key
   ```

5. Run the following command in your terminal to start the streamlit app:
   ```
   streamlit run app.py -w
   ```

   This will launch the Streamlit UI, allowing you to interact with the application.

   Enjoy! Cheers!
