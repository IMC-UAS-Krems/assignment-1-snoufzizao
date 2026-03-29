"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""
class StreamingPlatform:

    def __init__(self, name):
       
        self.name = name
        self.artists = []
        self.albums = []

    def add_artist(self, artist):
        self.artists.append(artist)

    def add_album(self, album):
        self.albums.append(album)

    def __str__(self):
        artist_list = "\n".join([f"{i+1}. {artist.name}" for i, artist in enumerate(self.artists)])
        album_list = "\n".join([f"{i+1}. {album.title} by {album.artist}" for i, album in enumerate(self.albums)])
        return f"Streaming Platform: {self.name}\nArtists:\n{artist_list}\nAlbums:\n{album_list}"