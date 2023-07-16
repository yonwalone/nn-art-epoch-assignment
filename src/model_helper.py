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


def get_image_count_of_epoch(pipeline_name, step_of_prep_pipe, epoch):
    """
    Get number of usable images for epoch.

    Args:
        pipeline_name (string): name of used preprocessing pipeline
        step_of_prep_pipe (string): name of the used step of the preprocessing pipeline
        epoch (string): name of used epoch

    Returns:
        int: number of images
    """
    try:
        return len(os.listdir(os.path.join(DATA_PATH, epoch, "images", pipeline_name, step_of_prep_pipe)))
    except:
        return 0
                