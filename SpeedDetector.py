import threading
import RPi.GPIO as GPIO
import time

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
    # GPIO pins
    TRIG_PIN = 17
    ECHO_PIN = 27

    # Set the mode and pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)

    while sd.on:
        speed = measure_speed()
        if speed is not None:
            sd.detected = True
            sd.detected_speed = speed
        time.sleep(0.05)


def measure_distance():
    # Send a short pulse to trigger the ultrasonic signal
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    # Wait for the echo signal
    pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    pulse_end = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    # Calculate the duration of the pulse
    pulse_duration = pulse_end - pulse_start

    # Speed of sound at 20 degrees Celsius (343 meters/second)
    speed_of_sound = 343.0

    # Calculate the distance (round-trip)
    distance = (pulse_duration * speed_of_sound) / 2.0

    return distance


def measure_speed():
    # Get the initial distance
    initial_distance = measure_distance()

    # Wait for some time (e.g., 1 second)
    time.sleep(0.01)

    # Get the final distance
    final_distance = measure_distance()

    # Calculate the speed
    speed = abs(final_distance - initial_distance) / 1.0  # Change in distance per second

    return speed