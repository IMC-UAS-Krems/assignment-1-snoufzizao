"""
tracks.py
---------
Implement the class hierarchy for all playable content on the platform.

Classes to implement:
  - Track (abstract base class)
    - Song
      - SingleRelease
      - AlbumTrack
    - Podcast
      - InterviewEpisode
      - NarrativeEpisode
    - AudiobookTrack
"""
class Track():
    def __init__(self, title, duration):
        self.title = title
        self.duration = duration

class Song(Track):
    def __init__(self, title, duration, artist):
        super().__init__(title, duration)
        self.artist = artist 

class SingleRelease(Song):
    def __init__(self, title, duration, artist):
        super().__init__(title, duration, artist)

class AlbumTrack(Song):
    def __init__(self, title, duration, artist, album):
        super().__init__(title, duration, artist)
        self.album = album

class Podcast(Track):
    def __init__(self, title, duration, host):
        super().__init__(title, duration)
        self.host = host

class InrerviewEpisode(Podcast):
    def __init__(self, title, duration, host, guest):
        super().__init__(title, duration, host)
        self.guest = guest

class NarrativeEpisode(Podcast):
    def __init__(self, title, duration, host, story):
        super().__init__(title, duration, host)
        self.story = story

class AudiobookTrack(Track):
    def __init__(self, title, duration, author):
        super().__init__(title, duration)
        self.author = author