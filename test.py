import jetson.inference
import jetson.utils

import shutil

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.85)
camera = jetson.utils.gstCamera(640,480,"/dev/video0")
display = jetson.utils.glDisplay()

catnum, dognum = 0, 0
savepath = './Photos'

while display.IsOpen():
	img, width, height = camera.CaptureRGBA()
	detections = net.Detect(img, width, height)

	for detection in detections:
		if detection.ClassID == 17 or detection.ClassID == 18:
			if detection.ClassID == 17:
				name = "Cat"
				catnum += 1
				file_name = name + str(catnum) + ".jpg"
			
			elif detection.ClassID == 18:
				name = "Dog"
				dognum += 1
				file_name = name + str(dognum) + ".jpg"


			jetson.utils.saveImage(file_name, img)
			shutil.move("./" + file_name, savepath + "/" + file_name)

	display.RenderOnce(img, width, height)
	display.SetTitle("Objection Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
