import serial
import subprocess
import sys
from time import sleep


def print_there(x, y, text):
    """ function to overide previous output"""
    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" %(x, y, text))
    sys.stdout.flush()


def connect():
    response = None
    while not response:
        sport = serial.Serial("/dev/ttyAMA0", 9600, timeout=1)
        try:
            response = sport.readlines(None)
            sport.close()
        except:
            sport.close()
        if not response:
            print("No serial data read")
            sleep(0.5)
    return response


def get_levels():
    response = connect()
    try:
        readings = response[0].decode(errors='replace').split()
    except:
        return None, None
    if readings and readings[0] == 'ID14' and len(readings) == 5:
        moisture_value = float(readings[2])
        light_value = float(readings[4])
    else:
        moisture_value = None
        light_value = None
    return moisture_value, light_value


def get_light_level():
    return get_levels()[1]


if __name__ == '__main__':
    subprocess.Popen("clear", shell=True)
    while True:
        response = connect()

        # print_there(1, 2, response)
        readings = response[0].decode().split()
        #print(readings)
        if readings and readings[0] == 'ID14' and len(readings) == 5:
            moisture_value = readings[2]
            light_value = readings[4]
            output = ' '.join(("Moisture%: ", moisture_value, " ", "Light%: ", light_value, " "))
            print_there(2, 2, output)
        sleep(1)
