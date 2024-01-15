from dotenv import load_dotenv
import os
from deepgram import DeepgramClient, PrerecordedOptions 
from flask import Flask, request, render_template, jsonify
import requests

load_dotenv('.env')
DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')
deepgram = DeepgramClient(DEEPGRAM_API_KEY)

audio = 'temp_audio.mp3'
 
def transcribe_audio_to_text(audio_file_path):
    try:
        
        with open(audio_file_path, 'rb') as buffer_data:
           payload = { 'buffer': buffer_data }

           options = PrerecordedOptions( model="nova-2", language="en-US")

           response = deepgram.listen.prerecorded.v('1').transcribe_file(payload, options)

           if response:
            text = response.results.channels[0].alternatives[0].transcript
            return text

    except Exception as e:
        return None, f"An exception occurred: {e}"
 
 
print(transcribe_audio_to_text(audio))
