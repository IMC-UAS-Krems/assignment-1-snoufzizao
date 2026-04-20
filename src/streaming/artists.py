from streaming.albums import Album


class Artist:
    
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
        
        album_id = f"{self.artist_id}-single-{len(self.albums) + 1}"
        single = Album(album_id, title, self, genre=genre, release_year=release_year)
        self.add_album(single)
        return single

