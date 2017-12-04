#!/usr/bin/python
# -*- coding: utf-8 -*

import subprocess
import shlex

SOUND_PATH = "/home/pi/Kidsbox"


def play_okay_sound():
    play_sound("Okay.wav")


def play_fault_sound():
    play_sound("Fault.wav")


def play_sound(sound_file):
    play_ok_command = "aplay {0}/{1}".format(SOUND_PATH, sound_file)
    subprocess.Popen(shlex.split(play_ok_command))
