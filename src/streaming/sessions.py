
class ListeningSession:
    
    def __init__(self, session_id, user, track, timestamp, duration_seconds):
        self.session_id = session_id
        self.user = user
        self.track = track
        self.timestamp = timestamp
        self.duration_listened_seconds = duration_seconds
    
    def duration_listened_minutes(self) -> float:
        """Return the duration listened in minutes (float)."""
        return float(self.duration_listened_seconds) / 60.0

