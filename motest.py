import RPi.GPIO as GPIO
import time


output_pin = 33

def main():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.HIGH)
	outp = 1

	print("PWM running. Press CTRL+C to exit.")
	try:
		while True:
			outp = not outp
			GPIO.output(output_pin, outp)
			time.sleep(0.0011)
	finally:
		GPIO.cleanup()

def motor(t, f, pin):
	num = round(t / (2.6 * f))
	outp = 1
	for i in range(num):
		GPIO.output(pin, outp)
		time.sleep(f)
		outp = not outp
		GPIO.output(pin, outp)
		time.sleep(f)
		outp = not outp

if __name__ == '__main__':
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.HIGH)
	motor(5, 0.0011, 33)
	GPIO.cleanup()


