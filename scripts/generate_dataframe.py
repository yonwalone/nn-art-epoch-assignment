import os
import csv
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers
from config import EPOCHS, PROJECT_ROOT
import src.model_helper as mh
import matplotlib.pyplot as plt
list = [os.path.join(epoch) for epoch in EPOCHS]

split_name="one_folder_only_resized_all_epochs"

def get_epochs_of_file(filename):
    splits = filename.split(";")
    epochs_of_file = []
    for split in splits:
        if split in EPOCHS:
            epochs_of_file.append(split)
    return epochs_of_file


def get_dataframe_of_files(input_directory):
    files = os.listdir(input_directory)
    with open(os.path.join(input_directory, 'dataframe.csv'), "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter="|", quotechar="$", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["filename", "labels"])
        for file in files:
            epochs_of_file = get_epochs_of_file(file)
            writer.writerow([file, epochs_of_file])




get_dataframe_of_files(os.path.join(PROJECT_ROOT, "data", "splits", split_name, "train"))
get_dataframe_of_files(os.path.join(PROJECT_ROOT, "data", "splits", split_name, "valid"))
get_dataframe_of_files(os.path.join(PROJECT_ROOT, "data", "splits", split_name, "test"))
