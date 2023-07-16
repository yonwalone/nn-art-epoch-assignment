import os
import random
import shutil
from config import EPOCHS, PROJECT_ROOT
import src.model_helper as mh


epoch_amount = 10 # Number of epochs to consider
split_name = "latest_resize_split" # Name of the split
using_pipeline = "3x384" # Name of the pipeline being used
using_step_of_prep_pipe = "resized" # Name of the step in the pipeline being used

# Split ratios for training, validation, and testing
train_split = 0.7
valid_split = 0.15
test_split = 0.15

# Whether to create separate folders for each epoch
one_folder_per_epoch = False

# Paths
DATA_PATH = os.path.join(PROJECT_ROOT, "data")
SPLIT_PATH = os.path.join(DATA_PATH, "splits", split_name)
TRAIN_PATH = os.path.join(SPLIT_PATH, "train")
VALID_PATH = os.path.join(SPLIT_PATH, "valid")
TEST_PATH = os.path.join(SPLIT_PATH, "test")

# Create necessary directories if they don't exist
os.makedirs(SPLIT_PATH, exist_ok=True)
os.makedirs(TRAIN_PATH, exist_ok=True)
os.makedirs(VALID_PATH, exist_ok=True)
os.makedirs(TEST_PATH, exist_ok=True)

# Sort the epochs in descending order based on the image count
epochs_sorted = sorted(
    EPOCHS, 
    key=lambda epoch: -mh.get_image_count_of_epoch(
        pipeline_name=using_pipeline, 
        step_of_prep_pipe=using_step_of_prep_pipe, 
        epoch=epoch
    )    
)

# Select a subset of epochs to use
used_epochs = epochs_sorted[:epoch_amount]

# Determine the minimum amount of images among the selected epochs
min_amount = mh.get_image_count_of_epoch(
    pipeline_name=using_pipeline, 
    step_of_prep_pipe=using_step_of_prep_pipe, 
    epoch=used_epochs[-1]
)

# Calculate the number of images for training, validation, and testing
train_amount = int(train_split * min_amount)
valid_amount = int(valid_split * min_amount)
test_amount = min_amount - train_amount - valid_amount

# Iterate over each art epoch
for art_epoch in used_epochs:
    # Define paths for the current epoch's train, valid, and test folders
    epoch_train_folder = os.path.join(TRAIN_PATH, art_epoch) if one_folder_per_epoch else TRAIN_PATH
    os.makedirs(epoch_train_folder, exist_ok=True)
    epoch_valid_folder = os.path.join(VALID_PATH, art_epoch) if one_folder_per_epoch else VALID_PATH
    os.makedirs(epoch_valid_folder, exist_ok=True)
    epoch_test_folder = os.path.join(TEST_PATH, art_epoch) if one_folder_per_epoch else TEST_PATH
    os.makedirs(epoch_test_folder, exist_ok=True)

    # Get the path of images for the current epoch
    images_path = os.path.join(DATA_PATH, art_epoch, "images", using_pipeline, using_step_of_prep_pipe)

    # Get all files in the images path
    all_files = os.listdir(images_path)

    # Randomly select a subset of files for the current epoch
    remaining_files = random.sample(all_files, min_amount)

    # Randomly select files for training
    train_list = random.sample(remaining_files, train_amount)
    for file in train_list:
        remaining_files.remove(file)

    # Randomly select files for validation
    valid_list = random.sample(remaining_files, valid_amount)
    for file in valid_list:
        remaining_files.remove(file)

    # The remaining files are used for testing
    test_list = remaining_files

    # Copy training images to the current epoch's train folder
    for train_image in train_list:
        file_path = os.path.join(images_path, train_image)
        shutil.copy(file_path, epoch_train_folder)
