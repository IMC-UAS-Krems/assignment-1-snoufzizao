
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
    def total_listening_time_minutes(self, start, end) -> float:
        total_seconds = 0
        for u in self.users:
            for s in getattr(u, "sessions", []):
                ts = getattr(s, "timestamp", None)
                if ts is None:
                    continue
                if start <= ts <= end:
                    total_seconds += getattr(s, "duration_listened_seconds", 0)
        return float(total_seconds / 60)

    # Q2
    def avg_unique_tracks_per_premium_user(self, days: int = 30) -> float:
        from datetime import datetime, timedelta

        now = datetime.now()
        cutoff = now - timedelta(days=days)
        premium_users = [u for u in self.users if u.__class__.__name__ == "PremiumUser"]
        if not premium_users:
            return 0.0
        counts = []
        for u in premium_users:
            tracks = {s.track.track_id for s in getattr(u, "sessions", []) if getattr(s, "timestamp", now) >= cutoff}
            counts.append(len(tracks))
        return float(sum(counts) / len(counts))

    # Q3
    def track_with_most_distinct_listeners(self):
        from collections import defaultdict

        listeners = defaultdict(set)
        for u in self.users:
            for s in getattr(u, "sessions", []):
                if getattr(s, "track", None) is None:
                    continue
                listeners[s.track.track_id].add(u.user_id)
        if not listeners:
            return None
        best_id = max(listeners.items(), key=lambda kv: len(kv[1]))[0]
        # find track object
        for t in self.tracks:
            if getattr(t, "track_id", None) == best_id:
                return t
        return None

    # Q4
    def avg_session_duration_by_user_type(self):
        from collections import defaultdict

        sums = defaultdict(int)
        counts = defaultdict(int)
        for u in self.users:
            tname = u.__class__.__name__
            for s in getattr(u, "sessions", []):
                sums[tname] += getattr(s, "duration_listened_seconds", 0)
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
        for u in self.users:
            # family members are instances of FamilyMember
            if u.__class__.__name__ == "FamilyMember" and (u.age is not None and u.age < age_threshold):
                for s in getattr(u, "sessions", []):
                    total_seconds += getattr(s, "duration_listened_seconds", 0)
        return float(total_seconds / 60)

    # Q6
    def top_artists_by_listening_time(self, n: int = 10):
        from collections import defaultdict

        #minutes as floats
        artist_seconds = defaultdict(float)
        for u in self.users:
            for s in getattr(u, "sessions", []):
                track = getattr(s, "track", None)
                if track is None:
                    continue
                #count only Song tracks
                from streaming.tracks import Song
                if isinstance(track, Song):
                    artist = getattr(track, "artist", None)
                    #for missing artist_id
                    artist_id = getattr(artist, "artist_id", None)
                    if artist_id is not None:
                        artist_seconds[artist] += getattr(s, "duration_listened_seconds", 0) / 60
        items = sorted(artist_seconds.items(), key=lambda kv: kv[1], reverse=True)
        return items[:n]

    # Q7
    def user_top_genre(self, user_id: str):
        user = next((u for u in self.users if u.user_id == user_id), None)
        if user is None:
            return None
        genre_seconds = {}
        total = 0
        for s in getattr(user, "sessions", []):
            g = getattr(s.track, "genre", None)
            secs = getattr(s, "duration_listened_seconds", 0)
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
        for p in self.playlists:
            from streaming.playlists import CollaborativePlaylist
            if not isinstance(p, CollaborativePlaylist):
                continue
            artists = set()
            from streaming.tracks import Song
            for t in p.tracks:
                if isinstance(t, Song):
                    a = getattr(t, "artist", None)
                    artist_id = getattr(a, "artist_id", None)
                    if artist_id is not None:
                        artists.add(artist_id)
            if len(artists) > threshold:
                result.append(p)
        return result

    # Q9
    def avg_tracks_per_playlist_type(self):
        from streaming.playlists import Playlist, CollaborativePlaylist
        counts = {"Playlist": [], "CollaborativePlaylist": []}
        for p in self.playlists:
            if isinstance(p, CollaborativePlaylist):
                counts["CollaborativePlaylist"].append(len(p.tracks))
            elif isinstance(p, Playlist):
                counts["Playlist"].append(len(p.tracks))
        return {
            "Playlist": float(sum(counts["Playlist"]) / len(counts["Playlist"])) if counts["Playlist"] else 0.0,
            "CollaborativePlaylist": float(sum(counts["CollaborativePlaylist"]) / len(counts["CollaborativePlaylist"])) if counts["CollaborativePlaylist"] else 0.0,
        }

    # Q10
    def users_who_completed_albums(self):
        result = []
        for u in self.users:
            completed = []
            listened = {s.track.track_id for s in getattr(u, "sessions", []) if getattr(s, "track", None) is not None}
            for album in self.albums:
                if not album.tracks:
                    continue
                album_track_ids = {t.track_id for t in album.tracks}
                if album_track_ids and album_track_ids.issubset(listened):
                    completed.append(album.title)
            if completed:
                result.append((u, completed))
        return result

    def __str__(self):
        artist_list = "\n".join([f"{i+1}. {artist.name}" for i, artist in enumerate(self.artists)])
        album_list = "\n".join([f"{i+1}. {album.title} by {album.artist}" for i, album in enumerate(self.albums)])
        return f"Streaming Platform: {self.name}\nArtists:\n{artist_list}\nAlbums:\n{album_list}"

