#!/usr/bin/python
# -*- coding: utf-8 -*

import glob
import os

import id3reader


def generate_dir_name(music_file):
    id3r = id3reader.Reader(music_file)
    album_name = id3r.getValue('album')
    return make_valid_directory_name(album_name)


def make_valid_directory_name(directory_name):
    # cause / are not allowed in dictionary
    return directory_name \
        .replace('/', '-') \
        .replace('\\', '-') \
        .replace('*', '-') \
        .replace(':', '_') \
        .replace('?', '') \
        .replace('<', '[') \
        .replace('>', ']') \
        .replace('|', '_')


def make_dir(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)


def move_files(music_file, directory_name):
    file_name = os.path.basename(music_file).decode("latin-1")
    file_dir = os.path.dirname(music_file).decode("latin-1")
    new_path = "." + file_dir + "\\" + directory_name + "\\" + file_name
    os.rename(music_file, new_path)


def move_mp3_to_album_dictionary(music_file):
    directory_name = generate_dir_name(music_file)
    make_dir(directory_name)
    move_files(music_file, directory_name)


def move_mp3s_to_album_dictionary():
    for music_file in glob.glob("*.mp3"):
        try:
            move_mp3_to_album_dictionary(music_file)
        except WindowsError:
            print music_file + " was not successful moved"
        finally:
            pass


# os.chdir(r"C:\Users\DENAGFEL\Desktop\p\sort\mu")
move_mp3s_to_album_dictionary()
raw_input('enter to exit:')
