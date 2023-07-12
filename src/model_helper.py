import os
import numpy as np

from config import EPOCHS, PROJECT_ROOT
DATA_PATH = os.path.join(PROJECT_ROOT, 'data')

def log(info, noprint=False):
    """
    Prints out the info and saves it in the log_file

    Args:
        info (string): The info which should be printed and logged.
        no_print (bool): Defines if the info should be printed out
    """
    info = str(info)
    if not noprint:
        print(info)

    log_file_path = os.path.join(DATA_PATH, "logs", "log.txt")
    with open(log_file_path, 'a') as log_file:
        log_file.write(info + "\n")

def load_image(filename):
    """
    Load and preprocess a single image

    Args:
        filename (string): filename of stored image
        label (string): label as string

    Returns:
        _type_: _description_
    """
    image = np.load(filename)["image"]
    labels = one_hot_encode(filename)

    return image, labels


def one_hot_encode(epoch_name):
    """
    Turns hot encoded array for epochs.

    Args:
        filename (_type_): _description_

    Returns:
        _type_: _description_
    """
    labels = [1 if epoch == epoch_name else 0 for epoch in EPOCHS]
    np_labels = np.array(labels)

    return np_labels

def get_used_files_of_log(input_file):
    used_files = []
    with open(input_file, 'r') as f_in:
        for line in f_in:
            if line.startswith("Used picture "):
                text = line[len("Used picture "):].strip()
                used_files.append(text)
    return list(set(used_files))

def get_image_count_of_epoch(pipeline_name, step_of_prep_pipe, epoch):
    try:
        return len(os.listdir(os.path.join(DATA_PATH, epoch, "images", pipeline_name, step_of_prep_pipe)))
    except:
        return 0
                