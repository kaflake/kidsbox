#!/usr/bin/python
# -*- coding: utf-8 -*

import playlistDictionary as pld

playlist_dictionary = pld.playlist_dictionary


def get_playlist_name(id):
    contains_playlist = id in playlist_dictionary
    playlist_name = "undefined"

    if contains_playlist:
        playlist_name = playlist_dictionary[id]

    return contains_playlist, playlist_name
