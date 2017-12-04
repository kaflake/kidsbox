#!/usr/bin/python
# -*- coding: utf-8 -*

import glob
import os

import id3reader


def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def move_files(music_file, album_name):
    file_name = os.path.basename(music_file).decode("latin-1")
    file_dir = os.path.dirname(music_file).decode("latin-1")
    new_path = "." + file_dir + "\\" + album_name + "\\" + file_name
    os.rename(music_file, new_path)


def move_files_to_album_dictionary(music_file):
    id3r = id3reader.Reader(music_file)
    album_name = id3r.getValue('album')
    make_dir(album_name)
    move_files(music_file, album_name)


os.chdir(r"C:\Users\DENAGFEL\Desktop\p\sort\mu")
for music_file in glob.glob("*.mp3"):
    try:
        move_files_to_album_dictionary(music_file)
    except WindowsError:
        print music_file + " was not successful moved"
    finally:
        pass


raw_input('enter to exit:')
