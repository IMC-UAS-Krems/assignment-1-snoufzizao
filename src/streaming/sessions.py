"""
sessions.py
-----------
Implement the ListeningSession class for recording listening events.

Classes to implement:
  - ListeningSession
"""
class ListeningSession():
    
    def __init__(self, user, start_time, end_time):
        self.user = user
        self.tracks = []
        self.start_time = start_time
        self.end_time = end_time

    def add_track(self, track):
        self.tracks.append(track)

    def __str__(self):
        track_list = "\n".join([f"{i+1}. {track}" for i, track in enumerate(self.tracks)])
        return f"Listening Session for {self.user} from {self.start_time} to {self.end_time}\nTracks:\n{track_list}"