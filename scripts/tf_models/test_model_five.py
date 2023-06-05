import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers
from config import EPOCHS, PROJECT_ROOT
import src.model_helper as mh
import matplotlib.pyplot as plt
# improve three_staplesv2

using_split = "only_resized_all_epochs"
model_name = "five_staplesv3Imp"
batch_size = 128
input_size = 224
SPLIT_PATH = os.path.join(PROJECT_ROOT, "data", "splits", using_split)

train_gen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.15,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.15,
    horizontal_flip=True
    )
valid_gen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
test_gen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)

train_batches = train_gen.flow_from_directory(
    os.path.join(SPLIT_PATH, "train"),
    target_size=(input_size, input_size),
    class_mode="sparse",
    batch_size=batch_size,
    shuffle=True,
    color_mode="rgb",
    classes=EPOCHS
)

valid_batches = train_gen.flow_from_directory(
    os.path.join(SPLIT_PATH, "valid"),
    target_size=(input_size, input_size),
    class_mode="sparse",
    batch_size=batch_size,
    shuffle=False,
    color_mode="rgb",
    classes=EPOCHS
)

test_batches = train_gen.flow_from_directory(
    os.path.join(SPLIT_PATH, "test"),
    target_size=(input_size, input_size),
    class_mode="sparse",
    batch_size=1,
    shuffle=False,
    color_mode="rgb",
    classes=EPOCHS
)

items = os.listdir(os.path.join(SPLIT_PATH, "train"))
# Filter the list to include only folders
folders = [item for item in items if os.path.isdir(os.path.join(SPLIT_PATH, "train", item))]
# Get the count of epoch folders
art_epoch_count = len(folders)


model = keras.models.load_model(os.path.join(PROJECT_ROOT, "results", f"five_staplesv3Imp.h5"))

# Training

model.evaluate(test_batches, verbose=1)