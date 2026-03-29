"""
artists.py
----------
Implement the Artist class representing musicians and content creators.

Classes to implement:
  - Artist
"""

from streaming.albums import Album


class Artist:  #musician or content creator, separate?
    def __init__(self, name, genre):
        self.name = name
        self.genre = genre
        self.albums = []

    def add_album(self, album):
        self.albums.append(album)

    def single_release(self, title, duration, genre=None, release_date=None):
        single = Album(title, self.name, genre=genre, release_date=release_date)
        self.add_album(single)
        return single

    def __str__(self): 
        album_list = "\n".join([f"{i+1}. {album.title}" for i, album in enumerate(self.albums)])
        return f"Artist: {self.name} ({self.genre})\nAlbums:\n{album_list}"