# Windows iTunes to macOS Music Importer

## Overview

This script will help you migrate your library from Windows iTunes to Mac Apple Music, the new app on Catalina. It is not a difficult thing to move all your files from one computer to another (lack of cables aside), but it is difficult to retain your play count info and seemingly impossible to keep your "Added on" dates. That is where this script comes in.

## Requirements

- `python3`
- macOS Catalina

## Setup

- Your Windows iTunes library must have been consolidated into one folder. If this is not the case, make sure you do so on the PC
- Copy its `iTunes Music Library.xml` file into the same directory as this one or specify where it is with `--xml_file_location`
- Move the folder encasing all of the artist folders into the same directory as this one or specify where it is with `--music_folder_location`

## Migrating your library 

- Run `migrate.py`

## Known issues

- This will not retain metadata for `WAV` files or recreate your playlists. It is not meant to. This is meant to only help with "Play count" and "Added on". Maybe at some point I will add support for that
