from darkflow.net.build import TFNet
from app.configuration import Configuration
from file_operations import File, Directory

# Command to run the training from the cmd:
# python flow --model cfg/tiny-yolo-voc-2c.cfg --load bin/tiny-yolo-voc.weights --train --annotation new_model_data/annotations --dataset new_model_data/images --gpu 0.8

def train_yolo_model():
    class_amount = len(File.read_labels(Configuration.get_selected_game()))
    model = File.get_yolo_cfg_file_fullpath(class_amount)
    label_path = File.get_yolo_label_textfile_fullpath(Configuration.get_selected_game())

    options = {
        'model': model,
        'load': 'bin/tiny-yolo-voc.weights',
        'annotation': Directory.get_annotation_directory(Configuration.get_selected_game()),
        'dataset': Directory.get_yolo_image_directory(Configuration.get_selected_game()),
        'labels': label_path,
        'gpu': 0.8
    }

    tfnet = TFNet(options)
    tfnet.train()   

if __name__ == "__main__":
    Configuration.set_selected_game('pong')
    train_yolo_model()
