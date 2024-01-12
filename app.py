import os
from flask import Flask, request, render_template, jsonify
from ytchat2 import download_youtube_video, convert_mp4_to_mp3, transcribe_audio_to_text, chat_with_bot, create_chatbot_context
from flask_cors import CORS

from dotenv import load_dotenv


load_dotenv('.env')

api_key = os.getenv('OPENAI_API_KEY')



app = Flask(__name__)
CORS(app)

CORS(app, resources={r"/*": {"origins": "*"}})

conversation_context = []

@app.route('/')
def index():
    return render_template('index.html') 


@app.route('/transcribe', methods=['POST'])
def transcribe_video():

    data = request.get_json()
    video_url = data.get('youtube_url')

    if not video_url:
        return jsonify({'error': 'Please provide a YouTube URL.'})

    # Download YouTube video
    video_path, download_error = download_youtube_video(video_url)
    if download_error:
        return jsonify({'error': download_error})

    # Convert video to audio
    audio_path, conversion_error = convert_mp4_to_mp3(video_path, 'temp_audio.mp3')
    if conversion_error:
        return jsonify({'error': conversion_error})

    # Transcribe audio to text
    transcribed_text, transcription_error = transcribe_audio_to_text(audio_path)
    if transcription_error:
        return jsonify({'error': transcription_error})

    global conversation_context
    conversation_context = create_chatbot_context(transcribed_text)

    return jsonify({'message': 'Transcription complete. You can now chat with the bot.'})


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('user_message')
    
    # Chat with the bot using the global conversation context
    global conversation_context
    try:
        bot_response = chat_with_bot(conversation_context, user_message)
        return jsonify({'bot_response': bot_response})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
