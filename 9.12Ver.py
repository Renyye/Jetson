import jetson.inference
import jetson.utils
import RPi.GPIO as GPIO
import time
import datetime

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
feed_flag = False  # 用于表示是否在投喂状态
last_catfeed_time = None
last_dogfeed_time = None
feed_interval = 10
frame_count = 0  # 用于计数连续的帧数

pin = 33
LED_G, LED_R = 31, 32
GPIO.setmode(GPIO.BOARD)
GPIO.setup([pin, LED_G, LED_R], GPIO.OUT)
GPIO.setup(LED_G, GPIO.OUT, initial=GPIO.HIGH)


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
             # print("Cat")
             time.sleep(0.1)
             cat_count, dog_count = 0, 0
             frame_count = 0
        elif dog_count >= detect_threshold:
             detected_ani = "Dog"
             # print("Dog")
             time.sleep(0.1)
             cat_count, dog_count = 0, 0
             frame_count = 0
        else:
             cat_count, dog_count = 0, 0
             frame_count = 0

    detected_ani = None
    display.RenderOnce(img, width, height)
    display.SetTitle(
        "Objection Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
    # return detected_ani


def record_feeding_time(output=''):
    current_time = time.strftime('%Y-%m-%d %H:%M:%S')
    with open('feeding_times.txt', 'a') as file:
        file.write(current_time + ' ' + output + '\n')


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

  # color为bool值，0亮红灯，1亮绿灯
# def lamp(pin, color):
#     if color:
#         GPIO.output()


def feed_cats():
    global feeding
    while True:
        if feed_flag and detected_ani == 'Cat' and (last_catfeed_time == None or time.time() - last_catfeed_time >= feed_interval):
            feeding = True
            last_catfeed_time = time.time()
            motor(2, 0.0011, 33)
            record_feeding_time('feeding cat')
            # print("Feeding the cats")
        feeding = False
        time.sleep(0.01)

def feed_dogs():
    global feeding,last_dogfeed_time
    while True:
        if feed_flag and detected_ani == 'Dog' and (last_dogfeed_time == None or time.time() - last_dogfeed_time >= feed_interval):
            feeding = True
            last_dogfeed_time = time.time()
            motor(2, 0.0011, 33)
            record_feeding_time('feeding dog')
        feeding = False
        time.sleep(0.01)

def cmd_in():
    global feed_flag
    while True:
        cmd = input("请输入操作指令, 1: 手动投喂, 2: 关闭自动投喂, 3: 终止程序\n")
        if cmd == '1':
            print("距离上次投喂猫已经过{:02d}时{:02d}分{:02d}秒".format(int((time.time()-last_catfeed_time)//3600), int((time.time()-last_catfeed_time)//60), int((time.time()-last_catfeed_time)%60)) )
            print("距离上次投喂狗已经过{:02d}时{:02d}分{:02d}秒".format(int((time.time()-last_dogfeed_time)//3600), int((time.time()-last_dogfeed_time)//60), int((time.time()-last_dogfeed_time)%60)) )
            op = None
            while op != '1' or op != '2' or op != '3':
                op = input("请输入投喂对象, 1: 猫, 2: 狗, 3: 返回上级页面\n")
                if op == '1':
                    feed_cats()
                elif op == '2':
                    feed_dogs()
                elif op == '3':
                    break

        elif cmd == '2':
            feed_flag = False
            print("自动投喂已关闭")
            pass

        elif cmd == '3':
            print("程序已终止")
            raise(KeyboardInterrupt)



feed_thrd = threading.Thread(target = feed_cats)
feed_thrd.start()
feed_thrd = threading.Thread(target = feed_dogs)
feed_thrd.start()
cmd_thrd = threading.Thread(target = cmd_in)
cmd_thrd.start()

while display.IsOpen():
    dect()

GPIO.cleanup()
