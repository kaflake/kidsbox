#!/usr/bin/python
# -*- coding: utf-8 -*

import RPi.GPIO as GPIO
import mpdClient
import playlistInterpreter
import soundControl

# Warnungen ausschalten
# GPIO.setwarnings(False)

# Pin Nummern verwenden
GPIO.setmode(GPIO.BOARD)
# Pin 11 als Input
GPIO.setup(13, GPIO.IN)
GPIO.setup(15, GPIO.IN)
GPIO.setup(16, GPIO.IN)
GPIO.setup(18, GPIO.IN)
GPIO.setup(19, GPIO.IN)
# GPIO.setup(33, GPIO.OUT) #debug output to show if its boot


def add_button_detect():
    GPIO.add_event_detect(13, GPIO.FALLING, callback=button_1_pressed, bouncetime=20)
    GPIO.add_event_detect(15, GPIO.FALLING, callback=button_2_pressed, bouncetime=20)
    GPIO.add_event_detect(16, GPIO.FALLING, callback=button_3_pressed, bouncetime=20)
    GPIO.add_event_detect(18, GPIO.FALLING, callback=button_4_pressed, bouncetime=20)
    GPIO.add_event_detect(19, GPIO.FALLING, callback=button_5_pressed, bouncetime=20)


def button_1_pressed(channel):
    mpdClient.play_pause_toggle()


def button_2_pressed(channel):
    mpdClient.next_title()


def button_3_pressed(channel):
    mpdClient.previous_title()


def button_4_pressed(channel):
    mpdClient.volume_up()


def button_5_pressed(channel):
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


add_button_detect()
mpdClient.wait_for_server_connection()  # do not, cause now it is set by mopidy audio
show_started_message()

try:
    read_playlist_loop()
finally:
    GPIO.cleanup()
