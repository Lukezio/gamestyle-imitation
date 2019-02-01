import time
import cv2
import numpy as np
import json
from PIL import ImageGrab
from darkflow.net.build import TFNet
from file_operations import File, Directory
from app.configuration import Configuration
from pynput.keyboard import Key, Controller, Listener
from pynput import keyboard as kb
from threading import Thread
import csv
from yolo_checkpoint import latest_checkpoint

activated_keys = {}
label_data_dict = {}
training_data = []
label_data = []

def save_training_data():
    dataset_file = File.get_training_dataset_fullpath(Configuration.get_selected_game())
    training_labels_file = File.get_training_labels_fullpath(Configuration.get_selected_game())
    print(dataset_file)
    print(training_labels_file)
    with open(dataset_file, 'w') as  myfile:
        wr = csv.writer(myfile, lineterminator='\n')
        for row in training_data:
            wr.writerow(row)

    with open(training_labels_file, 'w') as  myfile:
        wr = csv.writer(myfile, lineterminator='\n')
        for row in label_data:
            wr.writerow(row)
    

def detect_keys():
    with Listener(
                on_press=on_press,
                on_release=on_release) as listener:
            listener.join()

def on_press(key):
    if(str(key) in activated_keys):
        activated_keys[str(key)] = 1

def on_release(key):
    if(str(key) in activated_keys):
        activated_keys[str(key)] = 0
    if key == Key.esc:
        return False

def reset_label_dict(labels):
    for label in labels:
        label_data_dict[label] = (0.0, 0.0, 0.0, 0.0)

def reset_object_data():
    label_data = {}

def shorten_list(results):
    for result in results:
        label = result['label']
        if(label in label_data_dict):
            label_data_dict[label] = (result['topleft']['x'], result['topleft']['y'], result['bottomright']['x'], result['bottomright']['y'])
        else:
            raise Exception('An error occured while recording gameplay. Please check your labels.')

def append_training_data(labels, keys):
    temp = []
    for label in labels:
        temp.extend(label_data_dict[label])
    training_data.append(temp)

    temp2 = []
    for key in keys:
        temp2.append(activated_keys[key])
    label_data.append(temp2)

def capture():
    allowed_keys = File.read_keys(Configuration.get_selected_game())
    labels = File.read_labels(Configuration.get_selected_game())
    reset_label_dict(labels)
    
    for i in allowed_keys:
        activated_keys[i] = 0
    class_amount = len(File.read_labels(Configuration.get_selected_game()))
    model = File.get_yolo_cfg_file_fullpath(class_amount)
    label_path = File.get_yolo_label_textfile_fullpath(Configuration.get_selected_game())

    options = {
        'model': model,
        'load': latest_checkpoint(),
        'threshold': 0.2,
        'gpu': 0.8,
        'labels': label_path
    }

    tfnet = TFNet(options)
    color = (155, 155, 155)

    thread = Thread(target=detect_keys)
    thread.start()

    while True:
        img = ImageGrab.grab()
        img_np = np.array(img)

        frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

        results = tfnet.return_predict(frame)
        reset_label_dict(labels)
        shorten_list(results)
        print(results)
        #append data
        append_training_data(labels, allowed_keys)
          
        for label in  label_data_dict:
            tl = (int(label_data_dict[label][0]), int(label_data_dict[label][1]))
            br = (int(label_data_dict[label][2]), int(label_data_dict[label][3]))
            text = '{}'.format(label)
            frame = cv2.rectangle(frame, tl, br, color, 5)
            frame = cv2.putText(frame, text, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
            

        cv2.imshow("frame", frame)    

        if cv2.waitKey(1) == 27:
            break

    keyboard = Controller()
    keyboard.press(Key.esc)
    keyboard.release(Key.esc)
    cv2.destroyAllWindows()

    save_training_data()

if __name__ == "__main__":
    Configuration.set_selected_game('pong')
    capture()
