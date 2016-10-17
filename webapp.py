from flask import Flask, render_template, url_for, jsonify
from serial_reader import get_levels
from subprocess import call
# from water_plant import water_plant
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
PUMP = 4
GPIO.setup(PUMP, GPIO.OUT)


def water_plant(time):
    GPIO.output(PUMP, GPIO.HIGH)
    sleep(time)
    GPIO.output(PUMP, GPIO.LOW)

app = Flask(__name__)

moisture_value = 0
light_value = 0


@app.route('/_copy_photo/')
def copy():
    call(["bash", "/home/pi/PlantMonitor/copy_photo.sh"])
    message = "The image should now be in the gallery!"
    return jsonify(message)


@app.route('/_water_plant/')
def water():
    global moisture_value
    message = "Thanks for the drink. Cheers!"
    if float(moisture_value) > 50:
        message = "Sorry, I don't need any water right now"
    else:
        water_plant(1)
    return jsonify(message)


@app.route('/_get_readings/')
def get_readings():
    global moisture_value
    global light_value
    moisture, light = get_levels()
    if moisture and light:
        moisture_value = "{:.2f}".format(moisture)
        light_value = "{:.2f}".format(light)
    return jsonify(moisture_value, light_value)


@app.route('/')
def return_page():
    global moisture_value
    global light_value
    moisture, light = get_levels()
    if moisture and light:
        moisture_value = "{:.2f}".format(moisture)
        light_value = "{:.2f}".format(light)
        if float(moisture_value) < 50:
            water_plant(3)
    objects_to_render = {'css_url': url_for('static', filename='css/style.css'),
                         'images': url_for('static', filename='images/'),
                         'status': "I'm happy and I know it!",
                         'moisture': moisture_value,
                         'light': light_value,
                          }
    return render_template('index.html', **objects_to_render)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

