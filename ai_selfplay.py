from pynput.keyboard import Key, Controller, Listener
from file_operations import File
from app.configuration import Configuration
from keras_utils import create_model
import tensorflow as tf
import os
import cv2
from darkflow.net.build import TFNet
from PIL import ImageGrab
import numpy as np
from yolo_checkpoint import latest_checkpoint

running = False
label_data_dict = {}

def reset_label_dict(labels):
    for label in labels:
        label_data_dict[label] = (0.0, 0.0, 0.0, 0.0)

def shorten_list(results):
    for result in results:
        label = result['label']
        if(label in label_data_dict):
            label_data_dict[label] = (result['topleft']['x'], result['topleft']['y'], result['bottomright']['x'], result['bottomright']['y'])
        else:
            raise Exception('An error occured while recording gameplay. Please check your labels.')

def start_ai():
    global running
    keyboard = Controller()
    running = True
    keys = File.read_keys(Configuration.get_selected_game())
    labels = File.read_labels(Configuration.get_selected_game())
    model = create_model()
    dir = os.path.dirname(File.get_checkpoint_file(Configuration.get_selected_game()))
    latest = tf.train.latest_checkpoint(dir)
    model.load_weights(latest)

    class_amount = len(File.read_labels(Configuration.get_selected_game()))
    yolo_model = File.get_yolo_cfg_file_fullpath(class_amount)
    label_path = File.get_yolo_label_textfile_fullpath(Configuration.get_selected_game())

    options = {
        'model': yolo_model,
        'load': latest_checkpoint(),
        'threshold': 0.2,
        'gpu': 0.8,
        'labels': label_path
    }
    tfnet = TFNet(options)

    while running:
        img = ImageGrab.grab()
        img_np = np.array(img)
        frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        results = tfnet.return_predict(frame)
        reset_label_dict(labels)
        shorten_list(results)
        tensor = []
        for label in label_data_dict:
            tensor.append(int(label_data_dict[label][0]))
            tensor.append(int(label_data_dict[label][1]))
            tensor.append(int(label_data_dict[label][2]))
            tensor.append(int(label_data_dict[label][3]))
        #print(tensor)
        single_row = np.expand_dims(tensor, axis=0)
        retval = model.predict(single_row)[0]
        for index, val in enumerate(retval):
            mapped_key = get_key_code(keys[index])
            print(val)
            if(val < 0.5):
                keyboard.release(mapped_key)
                print('released: ' + str(mapped_key))
            if(val > 0.5):
                keyboard.press(mapped_key)
                print('pressed: ' + str(mapped_key))
        print(keys)
        print(retval)
    
    return



def stop_ai():
    global running
    running = False


def get_key_code(key):
    return {
        'Key.space': Key.space,
        'Key.tab': Key.tab,
        'Key.up': Key.up,
        'Key.alt': Key.alt,
        'Key.alt_gr': Key.alt_gr,
        'Key.alt_l': Key.alt_l,
        'Key.alt_r': Key.alt_r,
        'Key.backspace': Key.backspace,
        'Key.caps_lock': Key.caps_lock,
        'Key.cmd': Key.cmd,
        'Key.cmd_l': Key.cmd_l,
        'Key.cmd_r': Key.cmd_r,
        'Key.ctrl': Key.ctrl,
        'Key.ctrl_l': Key.ctrl_l,
        'Key.ctrl_r': Key.ctrl_r,
        'Key.delete': Key.delete,
        'Key.down': Key.down,
        'Key.end': Key.end,
        'Key.enter': Key.enter,
        'Key.esc': Key.esc,
        'Key.f1': Key.f1,
        'Key.f10': Key.f10,
        'Key.f11': Key.f11,
        'Key.f12': Key.f12,
        'Key.f13': Key.f13,
        'Key.f14': Key.f14,
        'Key.f15': Key.f15,
        'Key.f16': Key.f16,
        'Key.f17': Key.f17,
        'Key.f18': Key.f18,
        'Key.f19': Key.f19,
        'Key.f20': Key.f20,
        'Key.f2': Key.f2,
        'Key.f3': Key.f3,
        'Key.f4': Key.f4,
        'Key.f5': Key.f5,
        'Key.f6': Key.f6,
        'Key.f7': Key.f7,
        'Key.f8': Key.f8,
        'Key.f9': Key.f9,
        'Key.home': Key.home,
        'Key.insert': Key.insert,
        'Key.left': Key.left,
        'Key.menu': Key.menu,
        'Key.num_lock': Key.num_lock,
        'Key.page_down': Key.page_down,
        'Key.page_up': Key.page_up,
        'Key.pause': Key.pause,
        'Key.print_screen': Key.print_screen,
        'Key.right': Key.right,
        'Key.scroll_lock': Key.scroll_lock,
        'Key.shift': Key.shift,
        'Key.shift_l': Key.shift_l,
        'Key.shift_r': Key.shift_r
    }.get(key, key)


if __name__ == "__main__":
    Configuration.set_selected_game('pong')
    start_ai()
    