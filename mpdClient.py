#!/usr/bin/env python
# -*- coding: utf-8 -*

import socket
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 6600
BUFFER_SIZE = 1024

def connect_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    rec = s.recv(BUFFER_SIZE)
    print "received connection data:", rec
    return s


def send_command(command):
    s = connect_server()
    print "send " + command + " command"
    s.send(command + "\r\n")

    rec = s.recv(BUFFER_SIZE)
    print "received data:", rec

    s.close()
    return rec


def try_send_command(command):
    rec = ""
    try:
        rec = send_command(command)
    except:
        return False, rec
    else:
        return True, rec


def check_server_connection():
    try:
        s = connect_server()
        s.close()
    except:
        return False
    else:
        return True


def wait_for_server_connection():
    command_successful = check_server_connection()
    # cause on startup maybe mpd is not still started, so try to connect and till it is working
    while not command_successful:
        print "Retry connection"
        time.sleep(1)
        command_successful = check_server_connection()


def play_pause_toggle():
    return try_send_command("pause")


def reset_volume():
    result1 = try_send_command("volume -100")
    result2 = try_send_command("volume +10")
    return result1 and result2


def volume_up():
    return try_send_command("volume +5")


def volume_down():
    return try_send_command("volume -5")


def stop():
    return try_send_command("stop")


def play():
    return try_send_command("play")


def load_playlist(name):
    return try_send_command("load " + name)


def clear_playlist():
    return try_send_command("clear")


def next_title():
    return try_send_command("next")


def previous_title():
    return try_send_command("previous")


def is_rec_ok(rec):
    return rec.upper().startswith("OK")


def play_playlist(name):
    result1 = stop()
    result2 = clear_playlist()
    result3, rec = load_playlist('"' + name + '"')
    result4 = play()
    playlist_found = is_rec_ok(rec)
    return result1 and result2 and result3 and result4 and playlist_found
