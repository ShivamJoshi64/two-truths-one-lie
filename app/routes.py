from flask import Blueprint, request, jsonify
import moviepy.editor as mp
import speech_recognition as sr
import openai

main_routes = Blueprint('main', __name__)

# Route to handle video or audio input
@main_routes.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    file.save('temp_upload/' + file.filename)
    response = process_file(file.filename)

    return jsonify(response)

def process_file(filename):
    # Convert video to audio if needed and run processing
    if filename.endswith('.mp4'):
        video = mp.VideoFileClip('temp_upload/' + filename)
        video.audio.write_audiofile('temp_upload/audio.wav')
        audio_filename = 'temp_upload/audio.wav'
    else:
        audio_filename = 'temp_upload/' + filename

    transcription = speech_to_text(audio_filename)
    analysis = run_ai_analysis(transcription)

    return {'transcription': transcription, 'analysis': analysis}

def speech_to_text(audio_file):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
        return r.recognize_google(audio)

def run_ai_analysis(transcription):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Analyze the following transcription and detect the lie: {transcription}",
        max_tokens=50
    )
    return response.choices[0].text