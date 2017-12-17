#!/usr/bin/python
# -*- coding: utf-8 -*

import RPi.GPIO as GPIO
import time
import subprocess
import shlex
import mpdClient
import playlistInterpreter
import soundControl

# Warnungen ausschalten
# GPIO.setwarnings(False)

start_stop_button = 13
next_button = 16
previous_button = 15
volume_up_button = 18
volume_down_button = 19

start_start_button_press = None

# Pin Nummern verwenden
GPIO.setmode(GPIO.BOARD)
# Pin 11 als Input
GPIO.setup(start_stop_button, GPIO.IN)
GPIO.setup(next_button, GPIO.IN)
GPIO.setup(previous_button, GPIO.IN)
GPIO.setup(volume_up_button, GPIO.IN)
GPIO.setup(volume_down_button, GPIO.IN)
# GPIO.setup(33, GPIO.OUT) #debug output to show if its boot


# there is a hardware pullup -> listen on falling is first event
def add_button_detect():
    GPIO.add_event_detect(start_stop_button, GPIO.BOTH, callback=start_stop_pressed, bouncetime=200)
    GPIO.add_event_detect(next_button, GPIO.FALLING, callback=next_pressed, bouncetime=200)
    GPIO.add_event_detect(previous_button, GPIO.FALLING, callback=previous_pressed, bouncetime=200)
    GPIO.add_event_detect(volume_up_button, GPIO.FALLING, callback=volume_up_pressed, bouncetime=200)
    GPIO.add_event_detect(volume_down_button, GPIO.FALLING, callback=volume_down_pressed, bouncetime=200)


def start_stop_pressed(channel):
    mpdClient.play_pause_toggle()


#atm do not use this
def start_stop_toggle(channel):
    if GPIO.input(start_stop_button) == 0:
        on_start_stop_button_pressed()
    if GPIO.input(start_stop_button) == 1:
        on_start_stop_button_release()


def on_start_stop_button_pressed():
    global start_start_button_press
    start_start_button_press = time.time()
    # always toggle on falling (it the default command need to interpret directly)
    mpdClient.play_pause_toggle()


def on_start_stop_button_release():
    global start_start_button_press
    if start_start_button_press is not None:
        elapsed_in_s = time.time() - start_start_button_press
        start_start_button_press = None
        print "StartButton release after {0} sec".format(elapsed_in_s)
        if (elapsed_in_s >= 3) and (elapsed_in_s < 10):  # after 10 seconds ignore again, cause fault
            shutdown()


def next_pressed(channel):
    mpdClient.next_title()


def previous_pressed(channel):
    mpdClient.previous_title()


def volume_up_pressed(channel):
    mpdClient.volume_up()


def volume_down_pressed(channel):
    mpdClient.volume_down()


def show_started_message():
    # GPIO.output(33, GPIO.HIGH)
    soundControl.play_okay_sound()
    print "Successful startup mopidy connection"


def read_playlist_loop():
    while True:
        playlist_id = raw_input("Enter playlist: ")
        title = playlistInterpreter.get_playlist_name(playlist_id)
        if mpdClient.play_playlist(title):
            print "playlist {0} started".format(title)
            soundControl.play_okay_sound()
        else:
            print "playlist {0} not started".format(title)
            soundControl.play_fault_sound()


def shutdown():
    cmd = shlex.split("sudo shutdown -h now")
    subprocess.call(cmd, shell=True)


add_button_detect()
mpdClient.wait_for_server_connection()  # do not, cause now it is set by mopidy audio
show_started_message()

try:
    read_playlist_loop()
finally:
    GPIO.cleanup()
