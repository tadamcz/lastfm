from typing import Iterable

from pylast_subclass import Track


def null_mbid_frac(tracks: Iterable[Track]):
    counts = null_mbid_count(tracks)
    return {k: v / len(tracks) for k, v in counts.items()}


def null_mbid_count(tracks: Iterable[Track]):
    counts = {"artist": 0, "album": 0, "track": 0}
    for track in tracks:
        if track.artist.mbid is None:
            counts["artist"] += 1
        if track.album.mbid is None:
            counts["album"] += 1
        if track.mbid is None:
            counts["track"] += 1
    return counts
