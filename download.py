import datetime
import json
import os
import pickle

import humanize as humanize
import pylast
from dotenv import load_dotenv

load_dotenv()

# Obtain yours from https://www.last.fm/api/account/create for Last.fm
API_KEY = os.environ["LASTFM_API_KEY"]
API_SECRET = os.environ["LASTFM_API_SECRET"]
USERNAME = os.environ["LASTFM_USERNAME"]

network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)
user = network.get_user(USERNAME)


def to_dict(o: pylast.Track | pylast.PlayedTrack):
    """Follow the structure of pylast.PlayedTrack, even though I'm not sure why they use this two-level structure."""
    if isinstance(o, pylast.Track):
        return {"title": o.title, "artist": o.artist.name}
    if isinstance(o, pylast.PlayedTrack):
        return {
            "track": to_dict(o.track),
            "album": o.album,
            "playback_date": o.playback_date,
            "playback_timestamp": o.timestamp,
        }


def tracks_gen():
    time_to = datetime.datetime.now().timestamp()
    OLDEST = user.get_unixtime_registered()
    while time_to > OLDEST:
        print(f"Getting tracks played before {datetime.datetime.fromtimestamp(time_to)}... ", end="")
        tracks = user.get_recent_tracks(time_to=time_to, time_from=OLDEST, limit=500)
        print(f"got {len(tracks)} tracks")
        if not tracks:
            break
        for track in tracks:
            yield track
        time_to = int(tracks[-1].timestamp)



dir = "data"
stem = f"{dir}/{USERNAME}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
os.makedirs(dir, exist_ok=True)

# Currently, we're not making use of the fact it's a generator (we just turn it into a list).
# In the future, the generator could be used to stream the data to a file.
tracks = list(tracks_gen())
n_tracks_found = len(tracks)
api_play_count = user.get_playcount()
distance_frac = abs((n_tracks_found - api_play_count) / api_play_count)
print(f"Total: {n_tracks_found} tracks")

if n_tracks_found != api_play_count:
    print(f"Warning: number of tracks found ({n_tracks_found}) does not match API play count ({api_play_count}). "
          f"This is a {distance_frac * 100:.0f}% difference.")

with open(stem + ".pickle", "wb") as f:
    print("Running pickle.dump()...", end=" ")
    pickle.dump(tracks, f)
    print("done")

with open(stem + ".json", "w") as f:
    print("Running json.dump()...", end=" ")
    tracks = [to_dict(track) for track in tracks]
    json.dump(tracks, f, indent=2)
    print("done")

for ext in [".json", ".pickle"]:
    size = os.path.getsize(stem + ext)
    print(f"{stem + ext: <40} {humanize.naturalsize(size)}")