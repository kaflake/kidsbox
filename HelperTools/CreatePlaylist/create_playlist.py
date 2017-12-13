#!/usr/bin/python
# -*- coding: utf-8 -*

import glob
import os

import id3reader

playlist_path_prefix = "./music/"


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


dirnames = os.walk(".".decode('utf8')).next()[1]
for dirname in dirnames:
    playlist_name = dirname
    print "playlistname: " + playlist_name
    f = file(get_playlist_file_name(playlist_name), "w")
    playlist_dir_mp3 = ".\\" + dirname + "\\*.mp3"
    print playlist_dir_mp3
    for music_file in sorted(glob.glob(playlist_dir_mp3), key=get_track):
        print music_file
        music_file_path = playlist_path_prefix + playlist_name + "/" + os.path.basename(music_file)
        print music_file_path
        f.writelines(music_file_path.encode('utf8') + "\n")

    f.close()

