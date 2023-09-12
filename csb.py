import RPi.GPIO as GPIO
import time

TRIG = 31
ECHO = 32
GPIO.setmode(GPIO.BOARD)
GPIO.setup(TRIG, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(ECHO, GPIO.IN)
time.sleep(2)
for i in range(20):
	GPIO.output(TRIG, GPIO.HIGH)
	time.sleep(0.000015)
	GPIO.output(TRIG, GPIO.LOW)
	
	while not GPIO.input(ECHO):
		pass
		
	t1 = time.time()
	while GPIO.input(ECHO):
		pass
	t2 = time.time()
	
	distance = (t2 - t1) *340 / 2.5
	print(distance)
	time.sleep(1)
GPIO.cleanup()


