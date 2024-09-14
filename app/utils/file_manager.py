import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import VideosSearch
import yt_dlp
import os

# Spotify credentials
SPOTIFY_CLIENT_ID = '83c6ca7df97d4fb7be4f758aad013531'
SPOTIFY_CLIENT_SECRET = 'ea4653f27c9345b2bb7c389b710a9ab5'

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))


# Function to extract Spotify track ID from URL
def get_track_id_from_url(spotify_url):
    return spotify_url.split("/")[-1].split("?")[0]


# Function to get track details from Spotify using track ID
def get_spotify_track_details(track_id):
    track = sp.track(track_id)
    if track:
        track_info = {
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'spotify_url': track['external_urls']['spotify']
        }
        return track_info
    return None


# Function to search YouTube for a track using youtube-search-python
def search_youtube_video(track_name, artist_name):
    search_query = f"{track_name} {artist_name} official music video"
    videos_search = VideosSearch(search_query, limit=1)
    results = videos_search.result()

    if results['result']:
        video_id = results['result'][0]['id']
        youtube_link = f"https://www.youtube.com/watch?v={video_id}"
        return youtube_link
    return None


# Function to download audio from YouTube link
def download_audio_from_youtube(youtube_url, output_path='./'):
    # Ensure output folder exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    ydl_opts = {
        'verbose': True,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
       'socket_timeout': 30,
       'retries': 10,
       'fragment_retries': 10,
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),  # Save file to output_path
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])


# Main function to get Spotify track and download corresponding YouTube audio
def download_audio(spotify_url, output_folder='./'):
    # Extract track ID from Spotify URL
    track_id = get_track_id_from_url(spotify_url)

    # Get track details from Spotify
    spotify_track = get_spotify_track_details(track_id)
    
    if spotify_track:
        print(f"Found Spotify track: {spotify_track['name']} by {spotify_track['artist']}")
        
        # Search corresponding YouTube video
        youtube_link = search_youtube_video(spotify_track['name'], spotify_track['artist'])
        
        if youtube_link:
            print(f"Found YouTube link: {youtube_link}")
            
            # Download audio from YouTube and save it to the specified output folder
            download_audio_from_youtube(youtube_link, output_path=output_folder)
            print(f"Downloaded and saved audio in {output_folder} from: {youtube_link}")
        else:
            print("YouTube video not found.")
    else:
        print("Spotify track not found.")
