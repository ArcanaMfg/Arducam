from picamera2 import *
from null_preview import *
from time import sleep
from Focuser import Focuser
import cv2

def autofocus(f_s=0,f_e=41):
    focus=0
    max_val=0.0
    last_val=0.0
    cnt=0
    for i in range(f_s,f_e):
        focuser.set(Focuser.OPT_FOCUS, i*100)
        sleep(0.1)
        array = picam2.capture_array()
        image_g = cv2.cvtColor(array, cv2.COLOR_BGRA2GRAY)
        img_sobel = cv2.Sobel(image_g,cv2.CV_16U,1,1)
        val=cv2.mean(img_sobel)[0]

        if val > max_val:
           focus=i*100
           max_val = val

        if val < last_val:
           cnt+=1
        else:
           cnt=0

        if cnt > 6:
           focuser.set(Focuser.OPT_FOCUS, focus)
           sleep(0.1)
           #print(focus)
           break
        last_val = val
        #print(val)
    return focus


picam2 = Picamera2()
preview = NullPreview(picam2)
preview_config = picam2.preview_configuration()
capture_config = picam2.still_configuration()
picam2.configure(preview_config)
picam2.start()
focuser = Focuser('/dev/v4l-subdev1')
sleep(2)

autofocus()
picam2.switch_mode_and_capture_file(capture_config, "test.jpg")
