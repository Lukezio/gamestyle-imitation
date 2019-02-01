from file_operations import File, Directory
from app.configuration import Configuration
import os

def latest_checkpoint():
    class_amount = len(File.read_labels(Configuration.get_selected_game()))
    model = File.get_yolo_cfg_file_fullpath(class_amount)
    dir = Directory.get_yolo_checkpoint_directory()
    model_name = model[4:len(model) - 4]
    highest_ckpt = ''
    highest_ckpt_nr = 0
    for file in os.listdir(dir):
        endname = int(file.rfind('-'))
       
        if file.startswith(model_name[:endname]) and file.endswith("meta"):
            endpoint = int(file.rfind('.'))           
            cur_ckpt = int(file[endname + 1:endpoint])
            if cur_ckpt > highest_ckpt_nr:
                highest_ckpt_nr = cur_ckpt
                #highest_ckpt = os.path.join(dir, file)
                
        
    return highest_ckpt_nr


if __name__ == "__main__":
    Configuration.set_selected_game('pong')
    ckpt = latest_checkpoint()
    print(ckpt)

