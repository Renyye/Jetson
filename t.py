import time

last_catfeed_time = time.time()
time.sleep(2)
print("距离上次投喂猫已经过{:02d}时{:02d}分{:02d}秒".format( int((time.time()-last_catfeed_time)//3600), int((time.time()-last_catfeed_time)//60), int((time.time()-last_catfeed_time)%60)) )
