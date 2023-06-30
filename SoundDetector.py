import threading

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
    # use detector.detected to save positive results
    while detector.on:
        if pygame.mouse.get_pressed()[0]:
            detector.detected = True
            print("Sound detected")
