"""
playlists.py
------------
Implement playlist classes for organizing tracks.

Classes to implement:
  - Playlist
    - CollaborativePlaylist
"""
class Playlist:
    
    def __init__(self, name, creator):
        self.name = name
        self.creator = creator
        self.tracks = []
    
    def add_track(self, track):
        self.tracks.append(track)
    
    def __str__(self):
        track_list = "\n".join([f"{i+1}. {track}" for i, track in enumerate(self.tracks)])
        return f"Playlist: {self.name} by {self.creator}\nTracks:\n{track_list}"
    
class CollaborativePlaylist(Playlist):
    
    def __init__(self, name, creator):
        super().__init__(name, creator)
        self.collaborators = [creator]

    def add_collaborator(self, collaborator):
        if collaborator not in self.collaborators:
            self.collaborators.append(collaborator)
    
    def __str__(self):
        collaborator_list = ", ".join(self.collaborators)
        track_list = "\n".join([f"{i+1}. {track}" for i, track in enumerate(self.tracks)])
        return f"Collaborative Playlist: {self.name} by {self.creator}\nCollaborators: {collaborator_list}\nTracks:\n{track_list}"