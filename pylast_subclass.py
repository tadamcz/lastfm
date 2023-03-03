import collections

from pylast import User as _User, _extract, Track

PlayedTrack = collections.namedtuple(
    "PlayedTrack",
    ["track", "album", "playback_date", "timestamp", "mbid", "artist_mbid", "album_mbid"],
)


class User(_User):
    def _extract_played_track(self, track_node):
        title = _extract(track_node, "name")
        track_artist = _extract(track_node, "artist")
        date = _extract(track_node, "date")
        album = _extract(track_node, "album")
        timestamp = track_node.getElementsByTagName("date")[0].getAttribute("uts")

        mbid = _extract(track_node, "mbid") or None
        artist_mbid = track_node.getElementsByTagName("artist")[0].getAttribute("mbid") or None
        album_mbid = track_node.getElementsByTagName("album")[0].getAttribute("mbid") or None

        return PlayedTrack(
            Track(track_artist, title, self.network),
            album,
            date,
            timestamp,
            mbid,
            artist_mbid,
            album_mbid,
        )
