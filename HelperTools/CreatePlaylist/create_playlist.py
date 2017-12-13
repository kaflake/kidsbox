#!/usr/bin/python
# -*- coding: utf-8 -*

import glob
import os

import id3reader

playlist_path_prefix = "./music/"

# mainfolder = r"C:\Users\DENAGFEL\Desktop\p\sort\mu".decode('utf8')
# folder = r"C:\Users\DENAGFEL\Desktop\p\sort\Dann traut Euch - 7 klingende Hochzeitsgrüße".decode('utf8')
# os.chdir(folder)

# dirnames = os.walk(mainfolder).next()[1]
# print dirnames

def get_track(music_file):
    id3r = id3reader.Reader(music_file)
    track = id3r.getValue('track')
    return track


def get_actual_dir_name():
    splittedDir = os.getcwd().split('\\')
    length = len(splittedDir)
    dirname = splittedDir[length - 1]
    return dirname


def get_playlist_file_name(actual_dir):
    return actual_dir + ".m3u"


actual_dir = get_actual_dir_name()
f = file(get_playlist_file_name(actual_dir), "w")

for music_file in sorted(glob.glob("*.mp3"), key=get_track):
    music_file_path = playlist_path_prefix + actual_dir + "/" + music_file
    f.writelines(music_file_path + "\n")

f.close()

