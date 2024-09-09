def get_song_name(url):
    # Split the URL by '/' and get the last part
    last_part = url.split('/')[-1]
    
    # Split the last part by '.mp3' to get the song name
    song_name = last_part.split('.mp3')[0]
    
    return song_name

# Example usage:
url = "https://tsoul.com/wp-content/uploads/2024/05/Steady-As-A-Rock.mp3"
song_name = get_song_name(url)
print(song_name)