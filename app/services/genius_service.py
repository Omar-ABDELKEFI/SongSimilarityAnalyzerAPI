import requests
from dotenv import load_dotenv
import os

load_dotenv()


def get_lyrics(artist_name, song_title):
    try:
        response = requests.get(f"https://api.lyrics.ovh/v1/{artist_name}/{song_title}")
        data = response.json()
        if 'lyrics' in data:
            return data['lyrics']
        else:
            return None
    except Exception as e:
        print(f"Error fetching lyrics: {e}")
        return None
