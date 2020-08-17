import time

import cv2
from flask import render_template, Response

from piserver import app, cam
from my_hw.thermometer import get_temperature
from my_hw.camera import capture


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/temperature')
def temperature():
    return '{} °C'.format(get_temperature())

def generate():
    while True:
        frame = cam.get_latest_frame()
        if frame is None:
            continue
        success, img = cv2.imencode('.jpg', frame)
        if not success:
            continue
        yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + bytearray(img) + b'\r\n'

@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')
