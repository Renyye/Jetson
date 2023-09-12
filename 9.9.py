import jetson.inference
import jetson.utils
import RPi.GPIO as GPIO
import time

import shutil
import threading

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.90)
camera = jetson.utils.gstCamera(1280, 720, "/dev/video0")
display = jetson.utils.glDisplay()

savepath = './Photos'
catnum, dognum = 0, 0
detected_ani = None
cat_count = 0
dog_count = 0
detect_threshold = 10  # 设置投喂阈值
feeding = False  # 用于表示是否在投喂状态
last_feed_time = None
feed_interval = 3600
frame_count = 0  # 用于计数连续的帧数

pin = 33
LED = 29
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)
GPIO.setup(LED, GPIO.OUT, initial=GPIO.HIGH)


def dect():
    global cat_count, dog_count, frame_count, detected_ani

    img, width, height = camera.CaptureRGBA()
    detections = net.Detect(img, width, height)
    frame_count += 1

    for detection in detections:
        if detection.ClassID == 17 or detection.ClassID == 18:
            if detection.ClassID == 17:
                cat_count += 1
                # file_name = name + str(catnum) + ".jpg"

            elif detection.ClassID == 18:
                dog_count += 1
                # file_name = name + str(dognum) + ".jpg"
    
    if frame_count >= 20:
        if cat_count >= detect_threshold:
             detected_ani = "Cat"
             print("Cat")
             time.sleep(0.1)
        elif dog_count >= detect_threshold:
             detected_ani = "Dog"
             print("Dog")
             time.sleep(0.1)
        else:
             cat_count, dog_count = 0,0
             frame_count = 0
    
    detected_ani = None
    display.RenderOnce(img, width, height)
    display.SetTitle("Objection Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
    # return detected_ani


def record_feeding_time(output=''):
    global last_feed_time
    last_feed_time = time.time()
    current_time = time.strftime('%Y-%m-%d %H:%M:%S')
    with open('feeding_times.txt', 'a') as file:
        file.write(current_time + output + '\n')

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

def feed_cats():
    global feeding
    feeding = True
    if last_feed_time == None or time.time() - last_feed_time >= feed_interval:
        motor(2, 0.0011, 33)
        record_feeding_time('feeding cats')
        print("Feeding the cats")
    feeding = False
    time.sleep(0.01)

feed_thrd = threading.Thread(target = feed_cats)
feed_thrd.start()

while display.IsOpen():
    dect()

GPIO.cleanup()
