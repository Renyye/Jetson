import RPi.GPIO as GPIO
import time

LED = 29
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED, GPIO.OUT, initial = GPIO.LOW)

#GPIO.output(LED, GPIO.HIGH)
time.sleep(3)
GPIO.output(LED, GPIO.LOW)

GPIO.cleanup()

