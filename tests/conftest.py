"""
conftest.py
-----------
Shared pytest fixtures used by both the public and private test suites.
"""

import pytest
from datetime import date, datetime, timedelta

from streaming.platform import StreamingPlatform
from streaming.artists import Artist
from streaming.albums import Album
from streaming.tracks import (
    AlbumTrack,
    SingleRelease,
    InterviewEpisode,
    NarrativeEpisode,
    AudiobookTrack,
)
from streaming.users import FreeUser, PremiumUser, FamilyAccountUser, FamilyMember
from streaming.sessions import ListeningSession
from streaming.playlists import Playlist, CollaborativePlaylist


# ---------------------------------------------------------------------------
# Helper - timestamps relative to the real current time so that the
# "last 30 days" window in Q2 always contains RECENT sessions.
# ---------------------------------------------------------------------------
FIXED_NOW = datetime.now().replace(microsecond=0)
RECENT = FIXED_NOW - timedelta(days=10)   # well within 30-day window
OLD    = FIXED_NOW - timedelta(days=60)   # outside 30-day window


@pytest.fixture
def platform() -> StreamingPlatform:
    """Return a fully populated StreamingPlatform instance."""
    platform = StreamingPlatform("TestStream")

    # ------------------------------------------------------------------
    # Artists
    # ------------------------------------------------------------------
    pixels  = Artist("a1", "Pixels",    genre="pop")
    platform.add_artist(pixels)

    # ------------------------------------------------------------------
    # Albums & AlbumTracks
    # ------------------------------------------------------------------
    dd = Album("alb1", "Digital Dreams", artist=pixels, release_year=2022)
    t1 = AlbumTrack("t1", "Pixel Rain",      180, "pop",  pixels, track_number=1)
    t2 = AlbumTrack("t2", "Grid Horizon",    210, "pop",  pixels, track_number=2)
    t3 = AlbumTrack("t3", "Vector Fields",   195, "pop",  pixels, track_number=3)
    for track in (t1, t2, t3):
        dd.add_track(track)
        platform.add_track(track)
        pixels.add_track(track)
    platform.add_album(dd)

    # Additional albums (two albums, two songs each)
    sw = Album("alb2", "Silent Waves", artist=pixels, release_year=2021)
    s1 = AlbumTrack("t4", "Wave Crest", 200, "electronic", pixels, track_number=1)
    s2 = AlbumTrack("t5", "Low Tide",   230, "electronic", pixels, track_number=2)
    for track in (s1, s2):
        sw.add_track(track)
        platform.add_track(track)
        pixels.add_track(track)
    platform.add_album(sw)

    nn = Album("alb3", "Neon Nights", artist=pixels, release_year=2020)
    n1 = AlbumTrack("t6", "City Lights", 210, "synth", pixels, track_number=1)
    n2 = AlbumTrack("t7", "Midnight Drive", 185, "synth", pixels, track_number=2)
    for track in (n1, n2):
        nn.add_track(track)
        platform.add_track(track)
        pixels.add_track(track)
    platform.add_album(nn)


    # ------------------------------------------------------------------
    # Users
    # ------------------------------------------------------------------
    alice = FreeUser("u1", "Alice",   age=30)
    bob   = PremiumUser("u2", "Bob",   age=25, subscription_start=date(2023, 1, 1))
    # family account with a dependent (useful to exercise FamilyMember logic)
    carol = FamilyAccountUser("u3", "Carol", age=40)
    dave = FamilyMember("u4", "Dave", age=15, parent=carol)
    carol.add_sub_user(dave)

    for user in (alice, bob, carol, dave):
        platform.add_user(user)

    # ------------------------------------------------------------------
    # Listening sessions: two per user (mix of recent and old timestamps)
    # ------------------------------------------------------------------
    # Alice sessions
    a_s1 = ListeningSession("s1", alice, t1, RECENT, 120)
    a_s2 = ListeningSession("s2", alice, s1, OLD, 180)
    alice.add_session(a_s1)
    alice.add_session(a_s2)

    # Bob sessions (both recent to be counted in Premium stats)
    b_s1 = ListeningSession("s3", bob, t2, RECENT, 240)
    b_s2 = ListeningSession("s4", bob, s2, RECENT, 300)
    bob.add_session(b_s1)
    bob.add_session(b_s2)

    # Family member sessions (underage)
    f_s1 = ListeningSession("s5", dave, n1, RECENT, 150)
    f_s2 = ListeningSession("s6", dave, n2, OLD, 200)
    dave.add_session(f_s1)
    dave.add_session(f_s2)


    return platform


@pytest.fixture
def fixed_now() -> datetime:
    """Expose the shared FIXED_NOW constant to tests."""
    return FIXED_NOW


@pytest.fixture
def recent_ts() -> datetime:
    return RECENT


@pytest.fixture
def old_ts() -> datetime:
    return OLD
