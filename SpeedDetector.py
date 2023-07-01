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
    TRIG_PIN = 4
    ECHO_PIN = 17

    start_time = time.time()

    # Set the mode and pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)

    speed_list = []

    def check_still_running(sd):
        return sd.on

    while check_still_running(sd):
        speed = measure_speed()
        speed_list.append(speed)
        if speed is not None:
            print("Measured speed in while loop: " + str(speed))
            sd.detected_speed = max(speed_list)
        time.sleep(0.05)
        if time.time() - start_time > 3:
            sd.detected = True

    # GPIO.cleanup()


def measure_distance():
    TRIG_PIN = 4
    ECHO_PIN = 17

    # Send a short pulse to trigger the ultrasonic signal
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    # Wait for the echo signal
    test = time.time()
    pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()
        if time.time() - test > 0.5:
            return None

    test = time.time()
    pulse_end = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()
        if time.time() - test > 0.5:
            return None

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

    if initial_distance is None or final_distance is None:
        return None

    # Calculate the speed
    speed = abs(final_distance - initial_distance) / 0.01  # Change in distance per second

    print("Measured speed: " + str(speed))

    return speed