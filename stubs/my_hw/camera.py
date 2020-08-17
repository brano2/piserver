from shutil import copy
import os


def capture(save_dir:str='', filename:str='capture.jpg'):
    copy('/home/pi/Pictures/foo.jpg', os.path.join(save_dir, filename))
