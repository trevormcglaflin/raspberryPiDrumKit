from flask import Flask, render_template, request
import json
import RPi.GPIO as GPIO
import time
import numpy as np
from threading import Thread
import random


app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("drumkit.html")

# route for when user clicks "Rock on!"
@app.route("/play_drums", methods=["GET"])
def play_drums():
    bpm = request.values["bpm"]
    time_signature = request.values["time_signature"]

    # choose which loop to call based off of time signature given
    if time_signature == "44":
        fourfour(bpm)
    elif time_signature == "442":
        fourfourtwo(bpm)
    elif time_signature == "24":
        twofour(bpm)
    else:
        waltz(bpm)
    return json.dumps("Oh yeah....")

def fourfour(bpm):
    # establish pattern for fourfour time
    sequence = [
        [1, 0, 1],
        [0, 0, 0],
        [1, 0, 0],
        [0, 0, 0],
        [1, 1, 0],
        [0, 0, 0],
        [1, 0, 0],
        [0, 0, 0],
        [1, 0, 1],
        [0, 0, 0],
        [1, 0, 0],
        [0, 0, 0],
        [1, 1, 0],
        [0, 0, 0],
        [1, 0, 0],
        [0, 0, 0]
    ]
    # play beat
    play_beat(bpm, sequence)

def fourfourtwo(bpm):
    # establish a second pattern for fourfour time
    sequence = [
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 0],
        [0, 0, 0],
        [1, 1, 0],
        [0, 0, 0],
        [1, 0, 0],
        [0, 0, 0],
        [1, 0, 1],
        [0, 0, 0],
        [1, 0, 0],
        [0, 0, 0],
        [1, 1, 0],
        [0, 1, 0],
        [1, 1, 0],
        [0, 1, 0]
    ]
    # play beat
    play_beat(bpm, sequence)

def twofour(bpm):
    #establish the pattern for twofour time
    sequence = [
        [0, 0, 1],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [1, 1, 1],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 1],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [1, 1, 1],
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]
    #play beat
    play_beat(bpm, sequence)

def waltz(bpm):
     #establish the pattern for waltz time
     sequence = [
        [1, 0, 1],
        [0, 0, 0],
        [1, 1, 0],
        [0, 0, 0],
        [1, 1, 0],
        [0, 0, 0],
        [1, 0, 1],
        [0, 0, 0],
        [1, 1, 0],
        [1, 0, 0],
        [1, 1, 0],
        [0, 0, 0],
     ]
     # play beat
     play_beat(bpm, sequence)

# everything from here down is based off this link(with some modifications):
# https://www.instructables.com/A-Raspberry-Pi-Powered-Junk-Drum-Machine/
def play_beat(bpm, sequence):
    #map GPIO pins
    gpio_map = [2, 3, 4]

    #length of time that pin is activated
    active_duration = 0.01

    # Sets pin number to BCM mode
    GPIO.setmode(GPIO.BCM)

    # Calculate the time period between the solenoid being deactivated and the next beat starting
    beat_gap = ((float(60) / float(bpm)) - float(active_duration)) / 2

    #set each pin to low
    for i in gpio_map:
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i, GPIO.HIGH)

    #finally, run the loop
    try:
        for beat in infinite_generator(sequence):
            #get active drum numbers
            active = np.where(beat)[0]
            #get pin numbers for active drums
            pins = [gpio_map[i] for i in active]

            print("Activating Pins", pins)
            GPIO.output(pins, GPIO.LOW)
            time.sleep(active_duration)
            GPIO.output(pins, GPIO.HIGH)
            print('Sleep ', beat_gap)
            time.sleep(beat_gap)

    # end program when keyboard interrupt occurs
    except KeyboardInterrupt:
        print("Quit")
        #reset GPIO settings
        GPIO.cleanup()

# Generator to infinitely loop around the sequence
def infinite_generator(n):
    i = 0
    while True:
        if i >= len(n):
            i = 0

        yield n[i]
        i = i + 1