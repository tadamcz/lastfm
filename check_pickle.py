import glob
import os
import pickle

from tabulate import tabulate

from analyse import null_mbid_frac


def check(filename):
    with open(filename, "rb") as f:
        ptracks = pickle.load(f)
    print(f"Loaded {len(ptracks)} tracks from {filename}")
    print("First 3 tracks:")
    for track in ptracks[:3]:
        print(track)
    print("Last 3 tracks:")
    for track in ptracks[-3:]:
        print(track)

    fracs = null_mbid_frac([pt.track for pt in ptracks])
    print(tabulate(fracs.items(), headers=("Field", "Fraction null MBIDs"), floatfmt=".0%"))


def recent_pickle():
    files = glob.glob("data/*.pickle")
    files.sort(key=os.path.getmtime)
    return files[-1]


check(recent_pickle())
