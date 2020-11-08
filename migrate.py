#!/usr/bin/env python3

import argparse
import logging
import os
import plistlib
import subprocess
from datetime import datetime
from sys import exit
from urllib.parse import unquote

if __name__ == "__main__":

    # Parse the single argument
    p = argparse.ArgumentParser()
    p.add_argument("--music_folder_location", default="Music",
                   help="location of iTunes music folder whose contents will be imported into this Mac")
    p.add_argument("--xml_file_location", default="iTunes Music Library.xml",
                   help="location of Itunes Music Library.xml file that will be used to perform metadata correction")
    args = p.parse_args()

    # Set up logger
    logger = logging.getLogger(__name__)
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler("import.log")
    c_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.ERROR)
    format_ = '%(levelname)s - %(message)s'
    c_handler.setFormatter(logging.Formatter(format_))
    f_handler.setFormatter(logging.Formatter(format_))
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    logger.setLevel(logging.INFO)

    # Read XML file
    with open(args.xml_file_location, "rb") as f:
        music_library = plistlib.load(f)
    base_location = music_library["Music Folder"] + "Music"
    for track in [track[1] for track in music_library["Tracks"].items()]:
        try:
            # Get track details
            track_location = track["Location"]
            album = track["Album"]
            artist = track["Artist"]
            name = track["Name"]
            play_count = track.get("Play Count", 0)
            date_added = track["Date Added"]
            logger.info("== {} - {} ==\nLocation: {}\nPlay count: {}\nDate added: {}\n---".format(
                artist, name, track_location, play_count, date_added))
            mdhmy = datetime.strftime(date_added, "%m%d%H%M%y")
            corrected_track_location = os.path.join(args.music_folder_location, unquote(
                track_location).replace(unquote(base_location), ""))
            # Set computer date
            subprocess.run(["sudo", "date", "-u", mdhmy])
            logger.info("Set clock to {}".format(mdhmy))
            # Import into iTunes and correct play count
            subprocess.run(["osascript", "aaspc.applescript",
                            corrected_track_location, str(play_count)])
            logger.info("Imported file {} and set play count to {}".format(
                corrected_track_location, play_count))
        except KeyboardInterrupt:
            print("Import interrupted by user.")
            exit()
        except Exception as e:
            logger.exception(
                "An error occurred for {} - {}; skipping import".format(artist, name))
    subprocess.run(["sudo", "sntp", "-sS", "time.apple.com"])
    logger.info("Import complete; reset date. Please note you may have to add extra metadata and will definitely need to recreate your playlists!")
