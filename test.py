import RPi.GPIO as GPIO
import time


# PIN 11 (GPIO17) - MOUTH OPEN
# PIN 13 (GPIO27) - MOUTH CLOSED
# PIN 16 (GPIO23) - EYES OPEN
# PIN 18 (GPIO24) - EYES CLOSED

MOUTH_OPEN = 17
MOUTH_CLOSED = 27
EYES_OPEN = 23
EYES_CLOSED = 24

GPIO.setmode(GPIO.BOARD)

GPIO.setup(MOUTH_OPEN, GPIO.OUT)
GPIO.setup(MOUTH_CLOSED, GPIO.OUT)

GPIO.output(MOUTH_OPEN, GPIO.HIGH)
GPIO.output(MOUTH_CLOSED, GPIO.LOW)

time.sleep(3)

GPIO.output(MOUTH_OPEN, GPIO.LOW)
GPIO.output(MOUTH_CLOSED, GPIO.HIGH)

time.sleep(3)

GPIO.output(MOUTH_OPEN, GPIO.LOW)
GPIO.output(MOUTH_CLOSED, GPIO.LOW)

GPIO.cleanup()