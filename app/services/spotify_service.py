import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from app.utils import download_audio
import librosa
import numpy as np
import os
import asyncio
import concurrent.futures

def run_async(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

load_dotenv()

client_credentials_manager = SpotifyClientCredentials(
    client_id=os.getenv('SPOTIPY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET')
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def analyze_audio(audio_file):
    try:
        y, sr = librosa.load(audio_file)
        # Extract features
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        mfccs = librosa.feature.mfcc(y=y, sr=sr)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        return {
            'tempo': float(tempo),
            'spectral_centroid': float(np.mean(spectral_centroids)),
            'mfccs': mfccs.mean(axis=1).tolist(),
            'chroma': chroma.mean(axis=1).tolist()
        }
    except Exception as e:
        print(f"Error analyzing audio file {audio_file}: {e}")
        return {}


def get_top_five_songs(artist_name):
    results = sp.search(q=f'artist:{artist_name}', type='artist')
    if not results['artists']['items']:
        return None

    artist_id = results['artists']['items'][0]['id']
    top_tracks = sp.artist_top_tracks(artist_id)

    return top_tracks['tracks'][:5]

def analyze_and_cleanup(track_id):
    # Get track information from Spotify
    track_info = sp.track(track_id)
    print
    track_url = track_info['external_urls']['spotify']

    # Define the path to the 'dd' folder
    download_folder =  os.getcwd()+'/spotify_tracks'

    # Download the audio file
    print('Downloading audio...')
    download_audio(track_url, download_folder)
    print('Download complete.')

    # Find the downloaded file in the 'dd' folder
    downloaded_files = os.listdir(download_folder)

    if not downloaded_files:
        raise FileNotFoundError("No file found in the 'spotify_tracks' folder.")

    # Assuming there's only one file in the 'dd' folder after download
    download_path = os.path.join(download_folder, downloaded_files[0])

    try:
        # Analyze the downloaded audio
        audio_analysis = analyze_audio(download_path)
        return audio_analysis
    finally:
        # Ensure the file is deleted after analysis
        if os.path.exists(download_path):
            os.remove(download_path)
            print(f'{download_path} has been removed.')