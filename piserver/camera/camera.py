from threading import Lock

import cv2
from imutils.video import VideoStream
import numpy as np


class Camera:
    _stream: VideoStream

    def __init__(self):
        self._stream = VideoStream(usePiCamera=True, resolution=(820, 616))
        self._stream.start()

    def get_latest_frame(self):
        return self._stream.read()

    def stop(self):
        self._stream.stop()

    def __del__(self):
        self.stop()
