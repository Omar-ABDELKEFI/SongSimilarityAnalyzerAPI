from spotdl import Spotdl
import os 
obj = Spotdl(client_id="83c6ca7df97d4fb7be4f758aad013531", client_secret="ea4653f27c9345b2bb7c389b710a9ab5", no_cache=True)
song_objs = obj.search(["https://open.spotify.com/track/1zi7xx7UVEFkmKfv06H8x0"])
print(song_objs)
os.chdir('/workspace/SongSimilarityAnalyzerAPI/spotify_tracks')
obj.download_songs(song_objs)