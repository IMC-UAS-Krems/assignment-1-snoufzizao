"""
sessions.py
-----------
Implement the ListeningSession class for recording listening events.

Classes to implement:
  - ListeningSession
"""
class ListeningSession:
    """Represents a single listening event (one track listened by a user).

    Expected signature in tests:
      ListeningSession(session_id, user, track, timestamp, duration_seconds)
    """
    def __init__(self, session_id, user, track, timestamp, duration_seconds):
        self.session_id = session_id
        self.user = user
        self.track = track
        self.timestamp = timestamp
        self.duration_listened_seconds = duration_seconds

    def duration_listened_minutes(self):
        return self.duration_listened_seconds / 60

    def __str__(self):
        return f"ListeningSession({self.session_id}) user={self.user} track={self.track} ts={self.timestamp} dur={self.duration_listened_seconds}"