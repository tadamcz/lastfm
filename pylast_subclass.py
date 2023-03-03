import collections
from dataclasses import dataclass

from pylast import User as _User, _extract, Track

PlayedTrack = collections.namedtuple(
    "PlayedTrack",
    ["track", "album", "playback_date", "timestamp", "mbid", "artist_mbid", "album_mbid"],
)

@dataclass
class Artist:
    name: str
    mbid: str

@dataclass
class Album:
    title: str
    mbid: str

@dataclass
class Track:
    artist: Artist
    album: Album
    title: str
    mbid: str

@dataclass
class PlaybackDateTime:
    human: str
    unix: int

@dataclass
class PlayedTrack:
    track: Track
    playback_datetime: PlaybackDateTime

class User(_User):
    def _extract_played_track(self, track_node):
        title = _extract(track_node, "name")
        artist = _extract(track_node, "artist")
        album = _extract(track_node, "album")

        artist_mbid = track_node.getElementsByTagName("artist")[0].getAttribute("mbid") or None
        album_mbid = track_node.getElementsByTagName("album")[0].getAttribute("mbid") or None
        track_mbid = _extract(track_node, "mbid") or None

        artist = Artist(artist, artist_mbid)
        album = Album(album, album_mbid)
        track = Track(artist, album, title, track_mbid)

        date = _extract(track_node, "date")
        date_unix = int(track_node.getElementsByTagName("date")[0].getAttribute("uts") or None)
        playback_datetime = PlaybackDateTime(date, date_unix)

        return PlayedTrack(track, playback_datetime)
