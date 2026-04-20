

class Playlist:
    def __init__(self, playlist_id, title, owner=None):
        self.playlist_id = playlist_id
        self.title = title
        self.owner = owner
        self.tracks = []

    def add_track(self, track):
       
        if all(getattr(t, "track_id", None) != getattr(track, "track_id", None) for t in self.tracks):
            self.tracks.append(track)

    def remove_track(self, track_id: str):
        self.tracks = [t for t in self.tracks if getattr(t, "track_id", None) != track_id]

    def total_duration_seconds(self):
        return sum(getattr(t, "duration_seconds", 0) for t in self.tracks)

    def __str__(self):
        track_list = "\n".join([f"{i+1}. {track}" for i, track in enumerate(self.tracks)])
        return f"Playlist: {self.title} by {self.owner}\nTracks:\n{track_list}"


class CollaborativePlaylist(Playlist):
    def __init__(self, playlist_id, title, owner=None):
        super().__init__(playlist_id, title, owner=owner)
        #owner is first contributor if provided
        self.contributors = []
        if owner is not None:
            self.contributors.append(owner)

    def add_contributor(self, contributor):
        if contributor not in self.contributors:
            self.contributors.append(contributor)

    def remove_contributor(self, contributor):
        #never remove the owner
        if contributor == self.owner:
            return
        if contributor in self.contributors:
            self.contributors.remove(contributor)

    