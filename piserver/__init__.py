import atexit

stoppable_things = []
def cleanup():
    for thing in stoppable_things:
        thing.stop()

atexit.register(cleanup)

from flask import Flask

app = Flask(__name__)


from piserver.camera import Camera

cam = Camera()
stoppable_things.append(cam)


from piserver import routes
