from tkinter import *
from gui.start_window import StartWindow
from file_operations import Directory, File
from app.configuration import Configuration
from threading import Thread
import threading
from rectangle_selection import annotate_images
from capture_gameplay import capture
from train_yolo import train_yolo_model
from keras_utils import train
import csv
from ai_selfplay import start_ai, stop_ai

class GameOptionsWindow:


    def __init__(self, master):
        self.ai_running = False
        self.root = master
        self.is_annotating = False
        self.flag = threading.Event()
        self.thread = Thread(target=annotate_images)
        self.thread2 = Thread(target=start_ai)
        frame = Frame(master)
        frame.pack()
        Button(frame, text="Labels", command=self.show_object_list).grid(row=0)
        Button(frame, text="Record images", command=self.record_images).grid(row=1)
        Button(frame, text="Generate annotations", command=self.generate_annotations).grid(row=2)
        Button(frame, text="Train object detection", command=self.train_object_detection).grid(row=3)
        Button(frame, text="Keyboard Inputs", command=self.set_key_records).grid(row=4)
        Button(frame, text="Record gameplay data", command=capture).grid(row=5)
        Button(frame, text="Train gameplay style", command=self.train_gameplay_style).grid(row=6)
        self.run_ai_button = Button(frame, text="Run AI", command=self.run_ai)
        self.run_ai_button.grid(row=7)
        Label(frame).grid(row=8)
        Button(frame, text="Back", command=self.back_to_start_window).grid(row=9)

    def set_key_records(self):
        self.root.destroy()
        new_root = Tk()
        from gui.key_record_window import KeyRecordWindow
        app = KeyRecordWindow(new_root)
        new_root.mainloop()

    def record_images(self):
        self.root.destroy()
        new_root = Tk()
        from gui.screen_record import ScreenRecordWindow
        app = ScreenRecordWindow(new_root)
        new_root.mainloop()

    def show_object_list(self):
        if not File.yolo_label_file_exists(Configuration.get_selected_game()):
            File.create(Directory.get_label_directory(Configuration.get_selected_game()), File.YOLO_LABEL_TEXTFILE)
        self.root.destroy()
        new_root = Tk()
        from gui.labeling_window import LabelingWindow
        app = LabelingWindow(new_root)
        new_root.mainloop()

    def generate_annotations(self):
        #move method to thread
        self.is_annotating = not self.is_annotating
        if(self.is_annotating):
            self.thread.start()
        else:
            self.thread._stop()
            self.thread = Thread(target=annotate_images)
        #from rectangle_selection import annotate_images
        #annotate_images()
        #thread = Thread(target=annotate_images)
        #thread.start()
        


    def train_object_detection(self):
        File.create_yolo_config_file(Configuration.get_selected_game())
        train_yolo_model()
        
        
    def train_gameplay_style(self):
        dataset_file = File.get_training_dataset_fullpath(Configuration.get_selected_game())
        training_labels_file = File.get_training_labels_fullpath(Configuration.get_selected_game())

        with open(dataset_file, 'r') as f:
            reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
            dataset_list = list(reader)

        with open(training_labels_file, 'r') as f:
            reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
            labels_list = list(reader)

        train(dataset_list, labels_list)

    def run_ai(self):
        self.ai_running = not self.ai_running
        if self.ai_running:
            self.thread2.start()
            self.run_ai_button.config(text="Stop AI")
        else:
            stop_ai()
            self.thread2 = Thread(target=start_ai)
            self.run_ai_button.config(text="Run AI")


    def back_to_start_window(self):
        self.root.destroy()
        new_root = Tk()
        app = StartWindow(new_root)
        new_root.mainloop()
