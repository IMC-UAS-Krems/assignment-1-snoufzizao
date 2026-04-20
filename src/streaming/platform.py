from datetime import datetime, timedelta
from typing import List, Tuple


class StreamingPlatform:

    def __init__(self, name):
       
        self.name = name
        self.artists = []
        self.albums = []
        self.tracks = []
        self.users = []
        self.playlists = []

    def add_track(self, track):
        self.tracks.append(track)

    def add_user(self, user):
        self.users.append(user)
    
    def add_artist(self, artist):
        self.artists.append(artist)

    def add_album(self, album):
        self.albums.append(album)

    def add_playlist(self, playlist):
        self.playlists.append(playlist)

    def all_users(self):
        return list(self.users)

    # Q1
    def total_listening_time_minutes(self, start: datetime, end: datetime) -> float:
        """Return total listening time (minutes) for sessions between start and end (inclusive)."""
        total_seconds = 0
        for user in self.users:
            for session in getattr(user, "sessions", []):
                #ts is the session timestamp (datetime) or None
                ts = getattr(session, "timestamp", None)
                if ts is None:
                    continue
                if start <= ts <= end:
                    total_seconds += getattr(session, "duration_listened_seconds", 0) or 0
        return total_seconds / 60.0

    # Q2
    def avg_unique_tracks_per_premium_user(self, days: int = 30) -> float:
        """Average number of unique tracks listened to per PremiumUser in the last `days` days."""
        cutoff = datetime.now() - timedelta(days=days)
        premium = [user for user in self.users if user.__class__.__name__ == "PremiumUser"]
        if not premium:
            return 0.0

        totals = 0
        for user in premium:
            tracks = set()
            for session in getattr(user, "sessions", []):
                ts = getattr(session, "timestamp", None)
                if ts is None or ts < cutoff:
                    continue
                track = getattr(session, "track", None)
                if track is None:
                    continue
                tid = getattr(track, "track_id", None)
                if tid is not None:
                    tracks.add(tid)
            totals += len(tracks)

        return totals / len(premium)


    # Q3
    def track_with_most_distinct_listeners(self):
        from collections import defaultdict

        listeners = defaultdict(set)
        for user in self.users:
            for session in getattr(user, "sessions", []):
                if getattr(session, "track", None) is None:
                    continue
                listeners[session.track.track_id].add(user.user_id)
        if not listeners:
            return None
        best_id = max(listeners.items(), key=lambda kv: len(kv[1]))[0]
        #find track 
        for track in self.tracks:
            if getattr(track, "track_id", None) == best_id:
                return track
        return None

    # Q4
    def avg_session_duration_by_user_type(self):
        from collections import defaultdict

        sums = defaultdict(int)
        counts = defaultdict(int)
        for user in self.users:
            tname = user.__class__.__name__
            for session in getattr(user, "sessions", []):
                sums[tname] += getattr(session, "duration_listened_seconds", 0)
                counts[tname] += 1
        results = []
        for tname in sums.keys() | counts.keys():
            avg = float(sums.get(tname, 0) / counts.get(tname, 1)) if counts.get(tname, 0) > 0 else 0.0
            results.append((tname, avg))
        # sort descending by avg
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    # Q5
    def total_listening_time_underage_sub_users_minutes(self, age_threshold: int = 18) -> float:
        total_seconds = 0
        for user in self.users:
            #family members are instances of FamilyMember
            if user.__class__.__name__ == "FamilyMember" and (user.age is not None and user.age < age_threshold):
                for session in getattr(user, "sessions", []):
                    total_seconds += getattr(session, "duration_listened_seconds", 0)
        return float(total_seconds / 60)

    # Q6
    def top_artists_by_listening_time(self, n: int = 10):
        from collections import defaultdict

        #minutes as floats
        artist_seconds = defaultdict(float)
        for user in self.users:
            for session in getattr(user, "sessions", []):
                track = getattr(session, "track", None)
                if track is None:
                    continue
                #count only song tracks
                from streaming.tracks import Song
                if isinstance(track, Song):
                    artist = getattr(track, "artist", None)
                    #for missing artist_id
                    artist_id = getattr(artist, "artist_id", None)
                    if artist_id is not None:
                        artist_seconds[artist] += getattr(session, "duration_listened_seconds", 0) / 60
        items = sorted(artist_seconds.items(), key=lambda kv: kv[1], reverse=True)
        return items[:n]

    # Q7
    def user_top_genre(self, user_id: str):
        user = next((user for user in self.users if user.user_id == user_id), None)
        if user is None:
            return None
        genre_seconds = {}
        total = 0
        for session in getattr(user, "sessions", []):
            g = getattr(session.track, "genre", None)
            secs = getattr(session, "duration_listened_seconds", 0)
            if g is None:
                continue
            genre_seconds[g] = genre_seconds.get(g, 0) + secs
            total += secs
        if total == 0:
            return None
        top_genre = max(genre_seconds.items(), key=lambda kv: kv[1])[0]
        pct = (genre_seconds[top_genre] / total) * 100.0
        return (top_genre, float(pct))

    # Q8
    def collaborative_playlists_with_many_artists(self, threshold: int = 1):
        result = []
        for playlist in self.playlists:
            from streaming.playlists import CollaborativePlaylist
            if not isinstance(playlist, CollaborativePlaylist):
                continue
            artists = set()
            from streaming.tracks import Song
            for track in playlist.tracks:
                if isinstance(track, Song):
                    a = getattr(track, "artist", None)
                    artist_id = getattr(a, "artist_id", None)
                    if artist_id is not None:
                        artists.add(artist_id)
            if len(artists) > threshold:
                result.append(playlist)
        return result

    # Q9
    def avg_tracks_per_playlist_type(self):
        from streaming.playlists import Playlist, CollaborativePlaylist
        counts = {"Playlist": [], "CollaborativePlaylist": []}
        for playlist in self.playlists:
            if isinstance(playlist, CollaborativePlaylist):
                counts["CollaborativePlaylist"].append(len(playlist.tracks))
            elif isinstance(playlist, Playlist):
                counts["Playlist"].append(len(playlist.tracks))
        return {
            "Playlist": float(sum(counts["Playlist"]) / len(counts["Playlist"])) if counts["Playlist"] else 0.0,
            "CollaborativePlaylist": float(sum(counts["CollaborativePlaylist"]) / len(counts["CollaborativePlaylist"])) if counts["CollaborativePlaylist"] else 0.0,
        }

    # Q10
    def users_who_completed_albums(self):
        result = []
        for user in self.users:
            completed = []
            listened = {session.track.track_id for session in getattr(user, "sessions", []) if getattr(session, "track", None) is not None}
            for album in self.albums:
                if not album.tracks:
                    continue
                album_track_ids = {t.track_id for t in album.tracks}
                if album_track_ids and album_track_ids.issubset(listened):
                    completed.append(album.title)
            if completed:
                result.append((user, completed))
        return result

    def __str__(self):
        artist_list = "\n".join([f"{i+1}. {artist.name}" for i, artist in enumerate(self.artists)])
        album_list = "\n".join([f"{i+1}. {album.title} by {album.artist}" for i, album in enumerate(self.albums)])
        return f"Streaming Platform: {self.name}\nArtists:\n{artist_list}\nAlbums:\n{album_list}"

