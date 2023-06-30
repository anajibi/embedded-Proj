import threading


class SpeedDetector:
    detected = False
    detected_speed = None

    on = True

    def __init__(self):
        self.detected = False
        self.detected_speed = None

    def start_detection(self):
        thread = threading.Thread(target=detect_speed, args=[self])
        thread.start()

    def stop_detection(self):
        self.on = False

    def clear(self):
        self.detected = False
        self.detected_speed = None

    def is_speed_detected(self):
        return self.detected

    def turn_off(self):
        self.on = False

    def turn_on(self):
        self.on = True
        self.detected = False
        self.detected_speed = None

        self.start_detection()


def detect_speed(sd: SpeedDetector):
    while sd.on:
        pass
