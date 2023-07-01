import threading
import RPi.GPIO as GPIO
import time
import pygame.key


class SoundDetector:
    detected = False

    on = False

    def __init__(self):
        self.detected = False
        self.on = False

    def start_detection(self):
        # detect sound here and assign to self.detected
        # Create a new thread and start it
        thread = threading.Thread(target=detect_sound, args=[self])
        thread.start()

    def is_sound_detected(self):
        return self.detected

    def turn_off(self):
        self.on = False

    def turn_on(self):
        self.on = True
        self.detected = False

        self.start_detection()


def detect_sound(detector: SoundDetector):
    # GPIO SETUP
    channel = 27
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.IN)

    def callback(channel):
        if GPIO.input(channel):
            detector.detected = True
        else:
            detector.detected = True

    GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
    GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change

    # infinite loop
    while detector.on:
        time.sleep(1)

    GPIO.remove_event_callback(channel, callback)
    # GPIO.cleanup()  # clean up this should be tested TODO






