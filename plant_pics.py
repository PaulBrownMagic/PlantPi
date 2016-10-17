from time import sleep
from picamera import PiCamera

camera = PiCamera()
camera.hflip = True
camera.vflip = True
camera.start_preview()
for filename in camera.capture_continuous('/home/pi/PlantMonitor/static/plantpi.jpg'):
    print('Captured %s' % filename)
    sleep(60)
