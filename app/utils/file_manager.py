import os
from spotdl import Spotdl  # Assuming Spotdl is correctly imported from spotdl

# Initialize Spotdl object with appropriate client credentials
obj = Spotdl(client_id="83c6ca7df97d4fb7be4f758aad013531", 
             client_secret="ea4653f27c9345b2bb7c389b710a9ab5", 
             no_cache=True)

async def download_audio(track_url, download_path):
    # Save the current working directory
    print('eeeeeeeee')
    original_directory = os.getcwd()
    
    # Search for the song and get the song objects
    song_objs = obj.search([track_url])
    
    if not song_objs:
        print("No songs found for the given URL.")
        return

    print(song_objs)
    
    # Change to the desired download directory
    os.makedirs(download_path, exist_ok=True)  # Ensure the directory exists
    os.chdir(download_path)
    
    # Download the songs
    await obj.download_songs(song_objs)
    
    # Change back to the original directory
    os.chdir(original_directory)