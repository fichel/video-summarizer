# 📺 video-summarizer
Video Summarizer App that infers topics

The summarizarion works as follows:

1. User uploads a video (currently supports mp4 only)
2. Extract the audio and save it as mp3 by using moviepy (ffmpeg under the hood)
3. Extract the transcription from the mp3 using OpenAI's Audio transcription (Whisper) API 
4. Infer topics and summarize transcriptionusing OpenAI's Chatcompletion API 
