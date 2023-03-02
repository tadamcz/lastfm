import glob
import os
import pickle


def check(filename):
    with open(filename, "rb") as f:
        tracks = pickle.load(f)
    print(f"Loaded {len(tracks)} tracks from {filename}")
    print("First 3 tracks:")
    for track in tracks[:3]:
        print(track)
    print("Last 3 tracks:")
    for track in tracks[-3:]:
        print(track)


def recent_pickle():
    files = glob.glob("data/*.pickle")
    files.sort(key=os.path.getmtime)
    return files[-1]


check(recent_pickle())
