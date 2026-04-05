"""
albums.py
---------
Implement the Album class for collections of AlbumTrack objects.

Classes to implement:
  - Album
"""
class Album:

    def __init__(self, album_id, title, artist, genre=None, release_year=None):

        self.album_id = album_id
        self.title = title
        self.artist = artist
        self.genre = genre
        self.release_year = release_year
        self.tracks = []

    def add_track(self, track): 
        try: #to see if track belongs to album.
            track.album = self
        except Exception:
            pass

        self.tracks.append(track)
        # Keep tracks ordered by track_number when available.
        self.tracks.sort(key=lambda t: getattr(t, "track_number", 0))

    def __str__(self): # Return a string of the album, including its title, artist, and track list.
        
        track_list = "\n".join([f"{i+1}. {track}" for i, track in enumerate(self.tracks)])
        return f"Album: {self.title} by {self.artist}\nTracks:\n{track_list}"

    def track_ids(self):
        return {t.track_id for t in self.tracks}

    def duration_seconds(self):
        return sum(getattr(t, "duration_seconds", 0) for t in self.tracks)

class AlbumTrack(Album):

    def __init__(self, track_id, title, duration_seconds, genre, artist, track_number):

        self.track_id = track_id
        self.title = title
        self.duration_seconds = duration_seconds
        self.genre = genre
        self.artist = artist
        self.track_number = track_number
        self.album = None

    def __str__(self):  

        minutes = self.duration_seconds // 60 #type: ignore
        seconds = self.duration_seconds % 60 # type: ignore
        return f"{self.title} ({minutes}:{seconds:02d})"