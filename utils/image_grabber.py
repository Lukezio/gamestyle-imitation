from tkinter import *
import os
import time
import cv2
import numpy as np
from PIL import ImageGrab
from threading import Thread
from file_operations import Directory
from app.configuration import Configuration

class ImageGrabber(Thread):

    def __init__(self, *args, **kwargs):
        self.directory = Directory.get_screen_record_image_directory(Configuration.get_selected_game())
        super(ImageGrabber, self).__init__()
        _, _, files = next(os.walk(self.directory))
        self.cnt = len(files)
        print(self.cnt)
        self.running = False

    def set_started(self):
        self.running = True

    def set_stopped(self):
        self.running = False

    def run(self):
        while self.running:
            img = ImageGrab.grab()
            img_np = np.array(img)

            frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

            cv2.imshow("frame", frame)

            cv2.imwrite(os.path.join(self.directory, 'img_'  + str(self.cnt) + '.png'), frame)
            self.cnt += 1

            time.sleep(1)

            if cv2.waitKey(1) == 27:
                break

        cv2.destroyAllWindows()

    def stop(self):
        self.running = False

if __name__ == "__main__":
    thread = ImageGrabber()
    thread.set_started()
    thread.start()