import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers
from config import EPOCHS, PROJECT_ROOT
import pandas as pd
import src.model_helper as mh
import matplotlib.pyplot as plt

using_split = "one_folder_only_resized_all_epochs"
model_name = "multi_label"
batch_size = 128
input_size = 224
SPLIT_PATH = os.path.join(PROJECT_ROOT, "data", "splits", using_split)


train_data= pd.read_csv(os.path.join(SPLIT_PATH, "train", "dataframe.csv"), sep="|")

train_data['labels'] = train_data['labels'].apply(eval)  # Convert string representation of list to actual list
train_data_expanded = pd.DataFrame({
    'filename': np.repeat(train_data['filename'], train_data['labels'].apply(len)),
    'labels': np.concatenate(train_data['labels'].values)
})


valid_data= pd.read_csv(os.path.join(SPLIT_PATH, "valid", "dataframe.csv"), sep="|")
valid_data['labels'] = valid_data['labels'].apply(eval)  # Convert string representation of list to actual list
valid_data_expanded = pd.DataFrame({
    'filename': np.repeat(valid_data['filename'], valid_data['labels'].apply(len)),
    'labels': np.concatenate(valid_data['labels'].values)
})

test_data= pd.read_csv(os.path.join(SPLIT_PATH, "test", "dataframe.csv"), sep="|")
test_data['labels'] = test_data['labels'].apply(eval)  # Convert string representation of list to actual list
test_data_expanded = pd.DataFrame({
    'filename': np.repeat(test_data['filename'], test_data['labels'].apply(len)),
    'labels': np.concatenate(test_data['labels'].values)
})

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

train_batches = train_gen.flow_from_dataframe(
    dataframe=train_data_expanded,
    directory=os.path.join(os.path.join(SPLIT_PATH, "train")),
    target_size=(input_size, input_size),
    class_mode="categorical",
    shuffle=True,
    batch_size=batch_size,
    x_col="filename",
    y_col="labels",
    classes=EPOCHS
)

valid_batches = valid_gen.flow_from_dataframe(
    dataframe=valid_data_expanded,
    directory=os.path.join(os.path.join(SPLIT_PATH, "valid")),
    target_size=(input_size, input_size),
    class_mode="categorical",
    batch_size=batch_size,
    x_col="filename",
    y_col="labels",
    classes=EPOCHS
)

test_batches = test_gen.flow_from_dataframe(
    dataframe=test_data_expanded,
    directory=os.path.join(os.path.join(SPLIT_PATH, "test")),
    target_size=(input_size, input_size),
    class_mode="categorical",
    batch_size=batch_size,
    x_col="filename",
    y_col="labels",
    classes=EPOCHS
)


model = keras.models.load_model(os.path.join(PROJECT_ROOT, "results", f"multi_label.h5"))

# Training

model.evaluate(test_batches, verbose=1)