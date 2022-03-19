from picamera2 import *
from null_preview import *
from time import sleep
from Focuser import Focuser

picam2 = Picamera2()
preview = NullPreview(picam2)
preview_config = picam2.preview_configuration()
capture_config = picam2.still_configuration()

picam2.configure(preview_config)
picam2.start()
focuser = Focuser('/dev/v4l-subdev1')
sleep(2)

focuser.set(Focuser.OPT_FOCUS,1700) 
sleep(0.5)
picam2.switch_mode_and_capture_file(capture_config, "test1.jpg")
focuser.set(Focuser.OPT_FOCUS,4095)
sleep(0.5)
picam2.switch_mode_and_capture_file(capture_config, "test2.jpg") 