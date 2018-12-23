from flask import render_template

from app import app
from my_hw.thermometer import get_temperature


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/temperature')
def temperature():
    return '{} °C'.format(get_temperature())
