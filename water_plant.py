import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
PUMP = 4
GPIO.setup(PUMP, GPIO.OUT)


def water_plant(time):
    GPIO.output(PUMP, GPIO.HIGH)
    sleep(time)
    GPIO.output(PUMP, GPIO.LOW)


water_plant(3)
GPIO.cleanup()
