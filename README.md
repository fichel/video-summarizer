# video-summarizer
Video Summarizer App that infers topics

The summarizarion works as follows:

1. The user uploads a video (currently supports mp4 only)
2. The app uses moviepy (ffmpeg under the hood) to extract the audio and save an mp3
3. Uses OpenAI's Audio transcription (Whisper) API, it extracts the transcription from the mp3
4. Uses OpanAI's Chatcompletion api to summarize and infer topics
