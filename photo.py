from time import sleep
from picamera import PiCamera
from serial_reader import get_light_level

light = get_light_level()
if light:
    light = int(light)
else:
    sleep(2)
    light = get_light_level()
    if light:
        light = int(light)
    else:
        quit()

if light > 20:
    camera = PiCamera()
    camera.hflip = True
    camera.vflip = True
    camera.start_preview()
    sleep(1)
    camera.capture('/home/pi/PlantMonitor/static/plantpi.jpg')
    camera.stop_preview()
