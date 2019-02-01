from tkinter import *
import time
import cv2
import numpy as np
from PIL import ImageGrab
from threading import Thread
import threading
from utils.image_grabber import ImageGrabber

class ScreenRecordWindow:

    def __init__(self, master):
        self.is_recording = False
        self.flag = threading.Event()
        self.thread = ImageGrabber()
        self.root = master
        self.frame = Frame(master)
        self.frame.pack()
        self.record_button = Button(self.frame, text="Start recording", command=self.start_recording)
        self.record_button.grid(row=0, column=0)
        Label(self.frame).grid(row=0, column=1)
        Button(self.frame, text="Back", command=self.back_to_options_window).grid(row=0, column=2)

    def start_recording(self):
        self.is_recording = not self.is_recording
        if(self.is_recording):
            self.thread.set_started()
            self.thread.start()
            self.record_button.config(text="Stop recording")
        else:
            self.thread.set_stopped()
            self.thread = ImageGrabber(self.flag)
            self.record_button.config(text="Start recording")
        

    def back_to_options_window(self):
        self.thread.set_stopped()
        self.root.destroy()
        new_root = Tk()
        from gui.game_options_window import GameOptionsWindow
        app = GameOptionsWindow(new_root)
        new_root.mainloop()

if __name__ == "__main__":
    root = Tk()
    app = ScreenRecordWindow(root)
    root.mainloop()
