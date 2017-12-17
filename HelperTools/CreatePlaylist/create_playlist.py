#!/usr/bin/python
# -*- coding: utf-8 -*

import glob
import os

import id3reader

playlist_path_prefix = "./music/"


def get_track(music_file):
    id3r = id3reader.Reader(music_file)
    track = int(id3r.getValue('track'))
    return track


def get_actual_dir_name():
    splittedDir = os.getcwd().split('\\')
    length = len(splittedDir)
    dirname = splittedDir[length - 1]
    return dirname


def get_playlist_file_name(actual_dir):
    return actual_dir + ".m3u"


def get_music_file_path(music_file, playlist_name):
    return (playlist_path_prefix + playlist_name + "/" + os.path.basename(music_file)).encode('utf8') # linux path


def create_playlist(dir_name):
    playlist_name = dir_name
    f = file(get_playlist_file_name(playlist_name), "w")
    playlist_files_pattern = ".\\" + playlist_name + "\\*.mp3"  # windows path
    for music_file in sorted(glob.glob(playlist_files_pattern), key=get_track): # sort by track
        music_file_path = get_music_file_path(music_file, playlist_name)
        f.writelines(music_file_path + "\n")
    f.close()


dir_names = os.walk(".".decode('utf8')).next()[1]
for dir_name in dir_names:
    create_playlist(dir_name)

