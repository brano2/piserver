import time

import cv2
from flask import jsonify, render_template, request, Response

from piserver import app, cam
from my_hw.camera import capture
from my_hw.leds import ALL_LEDS
from my_hw.thermometer import Ds18b20


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/leds')
def leds_page():
    return render_template('leds.html')

@app.route('/leds/<led_id>/isOn')
def leds_query(led_id: str):
    if led_id not in ALL_LEDS:
        return jsonify({'message': f'Unknown LED ID: {led_id}',
                        'availableLeds': list(ALL_LEDS.keys())}), 404
    return jsonify({"ledId": led_id, "isOn": ALL_LEDS[led_id].is_lit})

@app.route('/leds/<led_id>/set')
def leds_set(led_id: str):
    if led_id not in ALL_LEDS:
        return jsonify({'message': f'Unknown LED ID: {led_id}',
                        'availableLeds': list(ALL_LEDS.keys())}), 404
    if 'on' not in request.args:
        return jsonify(message="URL parameter 'on' must be provided"), 400
    on: bool = request.args.get('on').lower() in ['true', 'yes', 't', 'y', '1']
    ALL_LEDS[led_id].value = on
    return jsonify({"ledId": led_id, "isOn": ALL_LEDS[led_id].is_lit})

@app.route('/temperature')
def temperature():
    return render_template('temperature.html')

@app.route('/temperature/readall')
def temperature_readall():
    return jsonify({t.id.hex(): t.get_temperature() for t in Ds18b20.get_all() if t.operational})

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
