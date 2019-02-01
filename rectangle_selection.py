import os
import cv2
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
from annotation_writer import write_xml
from bounding_box import BoundingBox
from point import Point
from file_operations import *

# global constants
IMG = None
OBJECT_LIST = []
OBJECTS = []
OBJECT = None

# constants
#IMAGE_FOLDER = 'data/images/geometry_dash'
#SAVE_DIRECTORY = 'data/annotations/geometry_dash'
#LABEL_DIRECTORY = 'data/labels/geometry_dash'


def line_select_callback(clk, rls):
    """Triggered whenever a rectangle is drawn"""
    global OBJECT
    extents = toggle_selector.RS.extents
    OBJECT = BoundingBox.create_from_points(
        Point(int(extents[0]), int(extents[2])), Point(int(extents[1]), int(extents[3])))
    print(OBJECT)

def onkeypress(event):
    """Triggered whenever a key is pressed"""
    global OBJECT_LIST
    global OBJECT
    global OBJECTS
    global IMG
    print(OBJECTS)
    print(len(OBJECTS))
    if event.key == '0':
        OBJECT.label = OBJECTS[0]
        OBJECT_LIST.append(OBJECT)
        print(OBJECT.label + ' ')
    if event.key == '1':
        OBJECT.label = OBJECTS[1]
        OBJECT_LIST.append(OBJECT)
        print(OBJECT.label + ' ')
    if event.key == '2':
        OBJECT.label = OBJECTS[2]
        OBJECT_LIST.append(OBJECT)
        print(OBJECT.label + ' ')
    if event.key == '3':
        OBJECT.label = OBJECTS[3]
        OBJECT_LIST.append(OBJECT)
        print(OBJECT.label + ' ')
    if event.key == '4':
        OBJECT.label = OBJECTS[4]
        OBJECT_LIST.append(OBJECT)
        print(OBJECT.label + ' ')
    if event.key == '5':
        OBJECT.label = OBJECTS[5]
        OBJECT_LIST.append(OBJECT)
        print(OBJECT.label + ' ')
    if event.key == '6':
        OBJECT.label = OBJECTS[6]
        OBJECT_LIST.append(OBJECT)
        print(OBJECT.label + ' ')
    if event.key == '7':
        OBJECT.label = OBJECTS[7]
        OBJECT_LIST.append(OBJECT)
        print(OBJECT.label + ' ')
    if event.key == '8':
        OBJECT.label = OBJECTS[8]
        OBJECT_LIST.append(OBJECT)
        print(OBJECT.label + ' ')
    if event.key == '9':
        OBJECT.label = OBJECTS[9]
        OBJECT_LIST.append(OBJECT)
        print(OBJECT.label + ' ')
    if event.key == 'q':
        print(OBJECT_LIST)
        write_xml(Directory.get_yolo_image_directory(Configuration.get_selected_game()), IMG, OBJECT_LIST, Directory.get_annotation_directory(Configuration.get_selected_game()))
        OBJECT_LIST = []
        IMG = None


def toggle_selector(event):
    toggle_selector.RS.set_active(True)


def annotate_images():
    global OBJECTS
    global IMG
    OBJECTS = File.read_labels(Configuration.get_selected_game())
    for n, image_file in enumerate(os.scandir(Directory.get_yolo_image_directory(Configuration.get_selected_game()))):
        IMG = image_file
        fig, ax = plt.subplots(1, figsize=(10.5, 8))
        
        image = cv2.imread(image_file.path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        ax.imshow(image)

        toggle_selector.RS = RectangleSelector(
            ax, line_select_callback,
            drawtype='box', useblit=True,
            button=[1], minspanx=5, minspany=5,
            spancoords='pixels', interactive=True,
        )
        bbox = plt.connect('key_press_event', toggle_selector)
        key = plt.connect('key_press_event', onkeypress)
        plt.tight_layout()
        plt.show()
        plt.close(fig)
    
    return
