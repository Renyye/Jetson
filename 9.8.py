import jetson.inference
import jetson.utils
import RPi.GPIO as GPIO
import time

import shutil

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.90)
camera = jetson.utils.gstCamera(1920,1080,"/dev/video0")
display = jetson.utils.glDisplay()

catnum, dognum = 0, 0
savepath = './Photos'

pin = 33
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)
LED = 29
GPIO.setup(LED, GPIO.OUT, initial = GPIO.HIGH)


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

while display.IsOpen():
	img, width, height = camera.CaptureRGBA()
	detections = net.Detect(img, width, height)

	for detection in detections:
		if detection.ClassID == 17 or detection.ClassID == 18:
			if detection.ClassID == 17:
				name = "Cat"
				catnum += 1
				file_name = name + str(catnum) + ".jpg"
				motor(2, 0.0011, 33)
			
			elif detection.ClassID == 18:
				name = "Dog"
				dognum += 1
				file_name = name + str(dognum) + ".jpg"


			jetson.utils.saveImage(file_name, img)
			shutil.move("./" + file_name, savepath + "/" + file_name)

	display.RenderOnce(img, width, height)
	display.SetTitle("Objection Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

GPIO.cleanup()

	
