# Chat with YT Videos

This project is an integration of various technologies to create an application that downloads YouTube videos, converts them to audio, transcribes the audio to text, and uses the transcribed text for chatbot conversations. It's built using Python, Flask, and APIs like Deepgram and OpenAI.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Vamsieth/ytchat.git
   ```
2. Installing dependencies:

   ```bash
    cd ytchat
    pip install -r requirements.txt
   ```

## Usage
1. Set up environment variables:

- Create a .env file in the root directory.
- Add your Deepgram and OpenAI API keys

   ```bash
   echo OPENAI_API_KEY=your_openai_api_key >> .env
   echo DEEPGRAM_API_KEY=your_deepgram_api_key >> .env
   ```

2. Run the flask server

   ```bash
   python app.py
   ```

3. Access the application via http://localhost:5000 in your web browser.

4. Use the UI to input a YouTube URL for transcription and chatbot interaction.

### APIs and Libraries Used

- Deepgram API: For audio transcription.
- OpenAI API: For chatbot responses.
- pytube: For downloading YouTube videos.
- moviepy: For converting video to audio.
- Flask: For the web server and API endpoints.

### Endpoints

1. Transcribe YouTube Video
- URL: /transcribe
- Method: POST
- Input: JSON with a YouTube URL
`
{
  "youtube_url": "https://www.youtube.com/watch?v=example_video_id"
}`
- Output: JSON response with success or error message.

2. Chat with Bot
- URL: /chat
- Method: POST
- Input: JSON with user message
`
{
  "user_message": "Summarize the video with bullet points in 250 words"
}
`