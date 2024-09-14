from flask import Blueprint, request, jsonify
from app.services import get_top_five_songs, analyze_and_cleanup, get_lyrics, analyze_audio , analyze_lyrics
from app.utils import calculate_similarity, get_song_name
from app import create_app
import io
import requests
import os
import uuid
from datetime import datetime
import shutil

# Create a Blueprint for the routes
routes = Blueprint('routes', __name__)

@routes.route('/compare-professor-song', methods=['POST'])
def compare_professor_song():
    singer_name = request.form.get('singer')
    professor_song_lyrics = request.form.get('lyrics')
    professor_song_url = request.form.get('songUrl')
    professor_song_file = request.files.get('songFile')
    # Validate that only one (either URL or File) is provided
    if (professor_song_url and professor_song_file) or (not professor_song_url and not professor_song_file):
        return jsonify({'error': 'Please provide either a song URL or an MP3 file, but not both'}), 400


    print('kkkk')
    # Create a unique folder name
    unique_id = str(uuid.uuid4())  # Generate a unique ID
    date_str = datetime.now().strftime('%Y%m%d_%H%M%S')  # Current date and time
    folder_name = f"{singer_name}_{date_str}_{unique_id}"
    download_folder = os.path.join(os.getcwd(), 'spotify_tracks', folder_name)

    # Create the unique folder
    os.makedirs(download_folder, exist_ok=True)
    print('nnn')

    try:
        # Handle song URL
        if professor_song_url and professor_song_url.lower().endswith('.mp3'):
            response = requests.get(professor_song_url)
            if response.headers.get('Content-Type') != 'audio/mpeg':
                return jsonify({'error': 'The URL does not point to a valid MP3 file'}), 400
            audio_bytes = io.BytesIO(response.content)
        # Handle MP3 file upload
        elif professor_song_file and professor_song_file.filename.lower().endswith('.mp3'):
            audio_bytes = io.BytesIO(professor_song_file.read())
        else:
            return jsonify({'error': 'You must provide a valid MP3 file or URL'}), 400

        # Analyze the song (either URL or file)
        professor_audio_analysis = analyze_audio(audio_bytes)
        print('rrrrrrrrrrrr')
        professor_song_data = {
            'name': professor_song_file.filename if professor_song_file else get_song_name(professor_song_url),
            'audio': professor_audio_analysis,
        }

        # Fetch top songs of the artist and compare
        top_songs = get_top_five_songs(singer_name)
        if not top_songs:
            return jsonify({'error': f'No songs found for the singer: {singer_name}'}), 404

        results = []
        for song in top_songs:
            # Pass the unique folder name to analyze_and_cleanup
            artist_audio_analysis = analyze_and_cleanup(song['external_urls']['spotify'], download_folder)
            # artist_lyrics = get_lyrics(song['artists'][0]['name'], song['name'])

            # if artist_lyrics is None:
            #     continue

            artist_song_data = {
                'name': song['name'],
                'audio': artist_audio_analysis,
            }

            similarity = calculate_similarity(professor_song_data, artist_song_data)

            results.append({
                'artist_song': song['name'],
                'professor_song': professor_song_data['name'],
                'similarity': similarity,
            })

        return jsonify(results)
    finally:
        # Ensure the folder is deleted after analysis
        if os.path.exists(download_folder):
            shutil.rmtree(download_folder)
            print(f'{download_folder} has been removed.')

@routes.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200