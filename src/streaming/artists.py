"""
artists.py
----------
Implement the Artist class representing musicians and content creators.

Classes to implement:
  - Artist
"""

class Artist:  #musician or content creator, separate?
    def __init__(self, name, genre):
        self.name = name
        self.genre = genre
        self.albums = []

    def add_album(self, album):
        self.albums.append(album)

    def __str__(self): 
        album_list = "\n".join([f"{i+1}. {album.title}" for i, album in enumerate(self.albums)])
        return f"Artist: {self.name} ({self.genre})\nAlbums:\n{album_list}"