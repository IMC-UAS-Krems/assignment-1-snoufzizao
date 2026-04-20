
class Album:

    def __init__(self, album_id, title, artist, genre=None, release_year=None):

        self.album_id = album_id
        self.title = title
        self.artist = artist
        self.genre = genre
        self.release_year = release_year
        self.tracks = []

    def add_track(self, track): 
        #
        try:
            setattr(track, "album", self)
        except Exception:
            pass

        self.tracks.append(track)
        #keep tracks ordered by track_number 
        self.tracks.sort(key=lambda t: getattr(t, "track_number", 0))

    def track_ids(self):
        return {t.track_id for t in self.tracks}

    def duration_seconds(self):
        return sum(getattr(t, "duration_seconds", 0) for t in self.tracks)


