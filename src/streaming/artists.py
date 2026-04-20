"""
artists.py
----------
Implement the Artist class representing musicians and content creators.

Classes to implement:
  - Artist
"""

from streaming.albums import Album


class Artist:
    """Represents an artist/content creator.

    Expected constructor signature used by tests: Artist(artist_id, name, genre="pop")
    """
    def __init__(self, artist_id, name, genre):
        self.artist_id = artist_id
        self.name = name
        self.genre = genre
        self.albums = []
        self.tracks = []

    def add_album(self, album):
        self.albums.append(album)

    def add_track(self, track):
        self.tracks.append(track)

    def track_count(self) -> int:
        return len(self.tracks)

    def single_release(self, title, duration, genre=None, release_year=None):
        single = Album(title, self.name, genre=genre, artist=self.name, release_year=release_year)
        self.add_album(single)
        return single

