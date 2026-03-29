"""
albums.py
---------
Implement the Album class for collections of AlbumTrack objects.

Classes to implement:
  - Album
"""
class Album:

    def __init__(self, title, artist):

        self.title = title
        self.artist = artist
        self.tracks = []

    def add_track(self, track): # Add a track to the album's track list.
    
        self.tracks.append(track)

    def __str__(self): # Return a string of the album, including its title, artist, and track list.
        
        track_list = "\n".join([f"{i+1}. {track}" for i, track in enumerate(self.tracks)])
        return f"Album: {self.title} by {self.artist}\nTracks:\n{track_list}"
