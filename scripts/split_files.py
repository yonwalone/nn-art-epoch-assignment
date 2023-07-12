import os
import random
import shutil
import numpy as np
import tensorflow as tf
from tensorflow import keras
from config import EPOCHS, PROJECT_ROOT
import src.model_helper as mh

epoch_amount = 10
split_name = "one_folder_only_resized_all_epochs"
using_pipeline = "3x224"
using_step_of_prep_pipe = "resized"
train_split = 0.7
valid_split = 0.15
test_split = 0.15
one_folder_per_epoch = False

DATA_PATH = os.path.join(PROJECT_ROOT, "data")
SPLIT_PATH = os.path.join(DATA_PATH, "splits", split_name)
TRAIN_PATH = os.path.join(SPLIT_PATH, "train")
VALID_PATH = os.path.join(SPLIT_PATH, "valid")
TEST_PATH = os.path.join(SPLIT_PATH, "test")

os.makedirs(SPLIT_PATH, exist_ok=True)
os.makedirs(TRAIN_PATH, exist_ok=True)
os.makedirs(VALID_PATH, exist_ok=True)
os.makedirs(TEST_PATH, exist_ok=True)

epochs_sorted = sorted(EPOCHS, key=lambda epoch: -mh.get_image_count_of_epoch(pipeline_name=using_pipeline, step_of_prep_pipe=using_step_of_prep_pipe, epoch=epoch))

used_epochs = epochs_sorted[:epoch_amount]

min_amount = mh.get_image_count_of_epoch(pipeline_name=using_pipeline, step_of_prep_pipe=using_step_of_prep_pipe, epoch=used_epochs[-1])

train_amount = int(train_split * min_amount)
valid_amount = int(valid_split * min_amount)
test_amount = min_amount - train_amount - valid_amount

for art_epoch in used_epochs:
    epoch_train_folder = os.path.join(TRAIN_PATH, art_epoch) if one_folder_per_epoch else TRAIN_PATH
    os.makedirs(epoch_train_folder, exist_ok=True)
    epoch_valid_folder = os.path.join(VALID_PATH, art_epoch) if one_folder_per_epoch else VALID_PATH
    os.makedirs(epoch_valid_folder, exist_ok=True)
    epoch_test_folder = os.path.join(TEST_PATH, art_epoch) if one_folder_per_epoch else TEST_PATH
    os.makedirs(epoch_test_folder, exist_ok=True)

    images_path = os.path.join(DATA_PATH, art_epoch, "images", using_pipeline, using_step_of_prep_pipe)
    all_files = os.listdir(images_path)
    remaining_files = random.sample(all_files, min_amount)

    train_list = random.sample(remaining_files, train_amount)
    for file in train_list:
        remaining_files.remove(file)
    valid_list = random.sample(remaining_files, valid_amount)
    for file in valid_list:
        remaining_files.remove(file)
    test_list = remaining_files

    for train_image in train_list:
        file_path = os.path.join(images_path, train_image)

        shutil.copy(file_path, epoch_train_folder)

    for valid_image in valid_list:
        file_path = os.path.join(images_path, valid_image)

        shutil.copy(file_path, epoch_valid_folder)
    
    for test_image in test_list:
        file_path = os.path.join(images_path, test_image)

        shutil.copy(file_path, epoch_test_folder)
