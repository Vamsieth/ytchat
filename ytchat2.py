from pytube import YouTube
from moviepy.editor import AudioFileClip
from openai import OpenAI
from dotenv import load_dotenv
import os



from deepgram import DeepgramClient, PrerecordedOptions 

load_dotenv('.env')

DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')
deepgram = DeepgramClient(DEEPGRAM_API_KEY)

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

# Function to download a YouTube video
def download_youtube_video(video_url):
    try:
        yt = YouTube(video_url)
        video_stream = yt.streams.filter(file_extension='mp4').first()
        if video_stream:
            video_path = video_stream.download(filename = 'temp_vid.mp4')  # This will use the default download path and filename
            return video_path, None  # No error
        else:
            return None, "No available video streams match the criteria."
    except Exception as e:
        return None, f"An error occurred: {e}"

# Function to convert MP4 to MP3
def convert_mp4_to_mp3(mp4_file_path, mp3_file_path):
    try:
        video_clip = AudioFileClip(mp4_file_path)
        video_clip.write_audiofile(mp3_file_path)
        video_clip.close()
        return mp3_file_path, None  # Indicate that there was no error
    except Exception as e:
        return None, f"An error occurred during conversion: {e}"

# Function to transcribe audio to text
def transcribe_audio_to_text(audio_file_path):
    try:
        
        with open(audio_file_path, 'rb') as buffer_data:
           payload = { 'buffer': buffer_data }

           options = PrerecordedOptions(
            smart_format=True, model="nova-2", language="en-US")


           response = deepgram.listen.prerecorded.v('1').transcribe_file(payload, options)

           if response:
            # Extract the transcription text
            text = response.results.channels[0].alternatives[0].transcript
            return text, None
           else:
            # Return None and the error message
             return None, f"An error occurred: {response} - {response.text}"

    except Exception as e:
        # Catch any exceptions and return None and the error message
        return None, f"An exception occurred: {e}"
# Function to create chatbot context from transcribed text
def create_chatbot_context(transcribed_text):
    return [{"role": "system", "content": transcribed_text}]

# Function to chat with the bot
def chat_with_bot(conversation, user_message):
    
    try:
        conversation.append({"role": "user", "content": user_message})
        response = client.chat.completions.create(model="gpt-3.5-turbo",  # replace with the correct model ID if different
        messages=conversation)
        assistant_message = response.choices[0].message.content
        conversation.append({"role": "assistant", "content": assistant_message})
        return assistant_message, None
    except Exception as e:
        return None, f"An error occurred: {e}"



