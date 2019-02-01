import os
import configparser
from app.configuration import Configuration

class File:

    YOLO_LABEL_TEXTFILE = 'labels.txt'
    YOLO_KEY_TEXTFILE = 'keys.txt'
    YOLO_CFG_FILE = 'tiny-yolo-voc{0}.cfg'
    TRAINING_LABELS_CSV_FILE = 'training_labels.csv'
    TRAINING_DATASET_CSV_FILE = 'dataset.csv'

    @staticmethod
    def create_yolo_config_file(game_name):
        default_config_file = File.get_default_config_file()
        with open(default_config_file) as f:
            content = f.readlines()
        print(content)
        print(len(content))

        #class_amount = int(content[119][8:])
        class_amount = len(File.read_labels(Configuration.get_selected_game()))
        print(str(class_amount))
        num = int(content[121][4:])
        filters = num * (class_amount + 5)
     #   content[119] = 'classes=' + str(class_amount) + '\n'
      #  content[113] = 'filters=' + str(filters) + '\n'
        content[119] = 'classes=' + str(class_amount) + '\n'
        content[113] = 'filters=' + str(filters) + '\n'

        print(content)

        with open(File.get_yolo_cfg_file_fullpath(class_amount), 'w') as f:
            f.write(''.join(content))

        #number_of_games = len(Configuration.PARSER.items('game-names'))
        #Configuration.PARSER.set('game-names', 'game_' + str(number_of_games + 1), str(game_name))
        #with open(Configuration.CONFIGURATION_FILE_PATH, "w") as configuration_file:
        #    Configuration.PARSER.write(configuration_file)
        #print('done')

    @staticmethod
    def get_default_config_file():
        return os.path.join(Directory.get_yolo_cfg_directory(), File.YOLO_CFG_FILE.format(''))

    @staticmethod
    def get_yolo_cfg_file_fullpath(class_amount = 0):
        return os.path.join(Directory.get_yolo_cfg_directory(), File.YOLO_CFG_FILE.format('-' + Configuration.get_selected_game() + ('-' + str(class_amount) + 'c' if  class_amount > 0 else '')))

    @staticmethod
    def read_labels(game_name):
        return [line.strip() for line in open(File.get_yolo_label_textfile_fullpath(game_name))]

    @staticmethod
    def read_keys(game_name):
        return [line.strip() for line in open(File.get_key_textfile_fullpath(game_name))]

    @staticmethod
    def create(directory, file):
        Directory.create(directory)
        full_path = File.full_path(directory, file)
        if(not os.path.exists(full_path)):
            open(full_path, 'w+')

    @staticmethod
    def full_path(directory, file):
        return os.path.join(directory, file)

    @staticmethod
    def get_yolo_label_textfile_fullpath(game_name):
        return os.path.join(Directory.get_label_directory(game_name), File.YOLO_LABEL_TEXTFILE)

    @staticmethod
    def get_key_textfile_fullpath(game_name):
        return os.path.join(Directory.get_key_directory(game_name), File.YOLO_KEY_TEXTFILE)

    @staticmethod
    def get_training_labels_fullpath(game_name):
        return os.path.join(Directory.get_training_labels_directory(game_name), File.TRAINING_LABELS_CSV_FILE)

    @staticmethod
    def get_training_dataset_fullpath(game_name):
        return os.path.join(Directory.get_training_dataset_directory(game_name), File.TRAINING_DATASET_CSV_FILE)

    @staticmethod
    def yolo_label_file_exists(game_name):
        return os.path.exists(File.get_yolo_label_textfile_fullpath(game_name))

    @staticmethod
    def add_label(entered_label):
        from app.configuration import Configuration
        file = open(File.get_yolo_label_textfile_fullpath(Configuration.get_selected_game()), 'a')
        file.write(entered_label + '\n')

    @staticmethod
    def add_key(key):
        from app.configuration import Configuration
        file = open(File.get_key_textfile_fullpath(Configuration.get_selected_game()), 'a')
        file.write(key + '\n')

    @staticmethod
    def get_checkpoint_file(game_name):
        return os.path.abspath("data/checkpoints/{0}/cp.ckpt").format(game_name)

class Directory:

    YOLO_IMAGE_DIRECTORY = 'data/images/{0}'
    YOLO_ANNOTATION_DIRECTORY = 'data/annotations/{0}'
    KEY_DIRECTORY = 'data/keys/{0}'
    YOLO_LABEL_DIRECTORY = 'data/labels/{0}'
    YOLO_DEFAULT_CHECKPOINT_DIRECTORY = 'ckpt'
    YOLO_DEFAULT_WEIGHTS_DIRECTORY = 'bin'
    YOLO_DEFAULT_MODELS_DIRECTORY = 'cfg'
    SCREEN_RECORD_IMAGE_DIRECTORY = 'data/images/{0}'
    TRAINING_DATA_DIRECTORY = 'data/training/{0}'
    CHECKPOINT_DATA_DIRECTORY = 'data/checkpoints/{0}'

    @staticmethod
    def get_yolo_checkpoint_directory():
        return Directory.YOLO_DEFAULT_CHECKPOINT_DIRECTORY

    @staticmethod
    def get_yolo_cfg_directory():
        return Directory.YOLO_DEFAULT_MODELS_DIRECTORY

    @staticmethod
    def get_screen_record_image_directory(game_name):
        return Directory.SCREEN_RECORD_IMAGE_DIRECTORY.format(game_name)

    @staticmethod
    def create(path):
        if(not os.path.isdir(path)):
            os.makedirs(path)

    @staticmethod
    def get_yolo_image_directory(game_name):
        return Directory.YOLO_IMAGE_DIRECTORY.format(game_name)

    @staticmethod
    def get_annotation_directory(game_name):
        return Directory.YOLO_ANNOTATION_DIRECTORY.format(game_name)

    @staticmethod
    def get_label_directory(game_name):
        return Directory.YOLO_LABEL_DIRECTORY.format(game_name)

    @staticmethod
    def get_key_directory(game_name):
        return Directory.KEY_DIRECTORY.format(game_name)

    @staticmethod
    def get_training_labels_directory(game_name):
        return Directory.TRAINING_DATA_DIRECTORY.format(game_name)

    @staticmethod
    def get_training_dataset_directory(game_name):
        return Directory.TRAINING_DATA_DIRECTORY.format(game_name)
        
    @staticmethod
    def create_game_directories(game_name):
        #directories = [Directory.YOLO_ANNOTATION_DIRECTORY, Directory.KEY_DIRECTORY, Directory.YOLO_LABEL_DIRECTORY, 
        #              Directory.SCREEN_RECORD_IMAGE_DIRECTORY, Directory.TRAINING_DATA_DIRECTORY, Directory.CHECKPOINT_DATA_DIRECTORY]
        #for directory in directories:
        Directory.create(Directory.YOLO_ANNOTATION_DIRECTORY.format(game_name))
        Directory.create(Directory.CHECKPOINT_DATA_DIRECTORY.format(game_name))
        Directory.create(Directory.YOLO_IMAGE_DIRECTORY.format(game_name))
        Directory.create(Directory.YOLO_LABEL_DIRECTORY.format(game_name))
        Directory.create(Directory.TRAINING_DATA_DIRECTORY.format(game_name))
        File.create(Directory.KEY_DIRECTORY.format(game_name), File.YOLO_KEY_TEXTFILE)
