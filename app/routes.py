from flask import Blueprint, request, jsonify
from app.services import get_top_five_songs, analyze_and_cleanup, get_lyrics, analyze_audio , analyze_lyrics
from app.utils import calculate_similarity, get_song_name
from app import create_app
import io
import requests


# Create a Blueprint for the routes
routes = Blueprint('routes', __name__)

@routes.route('/compare-professor-song', methods=['POST'])
def compare_professor_song():
    data = request.get_json()
    # Validate the input
    singer_name = data.get('singer_name')
    professor_song_url = data.get('professor_song_url')
    professor_song_lyrics = data.get('professor_song_lyrics')

    if not singer_name or not professor_song_url or not professor_song_lyrics:
        return jsonify({'error': 'Missing required parameters'}), 400

    # Validate the professor_song_url
    if not professor_song_url.lower().endswith('.mp3'):
        return jsonify({'error': 'The provided URL does not point to an MP3 file'}), 400

    response = requests.get(professor_song_url)
    
    # Check if the response is a valid MP3 file
    if response.headers.get('Content-Type') != 'audio/mpeg':
        return jsonify({'error': 'The URL does not point to a valid MP3 file'}), 400

    audio_bytes = io.BytesIO(response.content)
    print(audio_bytes, "audio_bytes-audio_bytes-audio_bytes-audio_bytes")
    
    # Analyze Professor Remember's song
    professor_audio_analysis = analyze_audio(audio_bytes)
    professor_song_data = {
        'name': get_song_name(professor_song_url),
        'audio': professor_audio_analysis,
        'lyrics': analyze_lyrics(professor_song_lyrics)
    }

    # Fetch top 5 songs of the provided singer
    top_songs = get_top_five_songs(singer_name)
    if not top_songs:
        return jsonify({'error': f'No songs found for the singer: {singer_name}'}), 404

    # Compare Professor Remember's song with each top song by the provided singer
    results = []
    for song in top_songs:
        # Analyze each of the top 5 songs
        artist_audio_analysis = analyze_and_cleanup(song['external_urls']['spotify'])
        artist_lyrics = get_lyrics(song['artists'][0]['name'], song['name'])

        if artist_lyrics is None:
            continue

        artist_song_data = {
            'name': song['name'],
            'audio': artist_audio_analysis,
            'lyrics': analyze_lyrics(artist_lyrics)
        }

        # Calculate similarity between Professor Remember's song and the artist's song
        similarity = calculate_similarity(professor_song_data, artist_song_data)

        results.append({
            'artist_song': song['name'],
            'professor_song': professor_song_data['name'],
            'similarity': similarity,
            'artist_lyrics': artist_lyrics
        })

    return jsonify(results)

@routes.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200