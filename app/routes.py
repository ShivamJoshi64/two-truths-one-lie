from flask import Blueprint, request, jsonify
import subprocess
import moviepy.editor as mp
import speech_recognition as sr
from openai import OpenAI
import os


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def home():
    return "Welcome to the 2T1L-app API!"

# Route to handle video or audio input
@main_routes.route('/upload', methods=['POST'])
def upload_file():
    # Check if the file is part of the request
    print(request.files)
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    # Get the file from the request
    file = request.files['file']

    # Check if the file has a valid name
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Check if a file was uploaded
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    # Save the file
    try:
        file.save('temp_upload/' + file.filename)
    except Exception as e:
        return jsonify({'file upload error': str(e)}), 500

    # Process the file and return the response
    response = process_file(file.filename)

    return jsonify(response)

def process_file(filename):
    # Define the path for the audio file
    audio_filename = 'temp_upload/audio.wav'

    # Convert video to audio if needed
    if filename.endswith('.mp4'):
        video = mp.VideoFileClip('temp_upload/' + filename)
        video.audio.write_audiofile(audio_filename)
    elif filename.endswith('.m4a'):
        # Convert M4A to WAV using FFmpeg
        try:
            subprocess.run(['ffmpeg', '-i', 'temp_upload/' + filename, audio_filename], check=True)
            print(f"Converted {filename} to {audio_filename}")
        except subprocess.CalledProcessError as e:
            print(f"Error converting file: {e}")
            return {'error': 'File conversion failed'}, 500
    else:
        # If the file is already in a compatible format, set the audio filename directly
        audio_filename = 'temp_upload/' + filename

    # Proceed with speech-to-text processing
    transcription = speech_to_text(audio_filename)
    analysis = run_ai_analysis(transcription)

    return {'transcription': transcription, 'analysis': analysis}

def speech_to_text(audio_file):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
        return r.recognize_google(audio)

def run_ai_analysis(transcription):
    response = client.chat.completions.create(model="gpt-4",  # Use "gpt-3.5-turbo" if GPT-4 is not available
    messages=[
        {"role": "system", "content": "You are a helpful assistant that analyzes speech transcripts to detect lies."},
        {"role": "user", "content": f"Analyze the following transcription and detect the lie: {transcription}"}
    ])
    return response.choices[0].message.content