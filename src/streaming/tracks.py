

class Track:
    def __init__(self, track_id, title, duration_seconds, genre):
        self.track_id = track_id
        self.title = title
        self.duration_seconds = duration_seconds
        self.genre = genre

    def duration_minutes(self):
        return self.duration_seconds / 60

    def __eq__(self, other):
        if not isinstance(other, Track):
            return False
        return self.track_id == other.track_id

    def __repr__(self):
        return f"Track({self.track_id!r}, {self.title!r}, {self.duration_seconds!r}, {self.genre!r})"


class Song(Track):
    def __init__(self, track_id, title, duration_seconds, genre, artist):
        super().__init__(track_id, title, duration_seconds, genre)
        self.artist = artist


class SingleRelease(Song):
    def __init__(self, track_id, title, duration_seconds, genre, artist, release_date=None):
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.release_date = release_date


class AlbumTrack(Song):
    def __init__(self, track_id, title, duration_seconds, genre, artist, track_number):
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.track_number = track_number
        self.album = None


class Podcast(Track):
    def __init__(self, track_id, title, duration_seconds, genre, host, description=""):
        super().__init__(track_id, title, duration_seconds, genre)
        self.host = host
        self.description = description


class InterviewEpisode(Podcast):
    def __init__(self, track_id, title, duration_seconds, genre, host, guest=None, description=""):
        super().__init__(track_id, title, duration_seconds, genre, host, description=description)
        self.guest = guest


class NarrativeEpisode(Podcast):
    def __init__(self, track_id, title, duration_seconds, genre, host, season=None, episode_number=None, description=""):
        super().__init__(track_id, title, duration_seconds, genre, host, description=description)
        self.season = season
        self.episode_number = episode_number


class AudiobookTrack(Track):
    def __init__(self, track_id, title, duration_seconds, genre, author, narrator=None):
        super().__init__(track_id, title, duration_seconds, genre)
        self.author = author
        self.narrator = narrator