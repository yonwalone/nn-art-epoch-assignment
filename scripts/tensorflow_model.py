
import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.utils import to_categorical
from config import EPOCHS, PROJECT_ROOT


DATA_PATH = os.path.join(PROJECT_ROOT, "data")

input_shape = (224, 224, 3)
num_art_epochs = 10
batch_size = 32

# Create a list of filenames and labels for all images
filenames = []
labels = []
for epoch in range(num_art_epochs):
    data = np.load(f"epoch_{epoch}.npz")
    epoch_filenames = data["filenames"]
    epoch_labels = data["labels"]
    filenames += epoch_filenames.tolist()
    labels += epoch_labels.tolist()

# Create a dataset of filenames and labels
dataset = tf.data.Dataset.from_tensor_slices((filenames, labels))

# Shuffle the dataset
dataset = dataset.shuffle(len(filenames))

# Load and preprocess the images in parallel
dataset = dataset.map(load_image, num_parallel_calls=tf.data.experimental.AUTOTUNE)

# Batch the dataset
dataset = dataset.batch(batch_size)

# Split the dataset into training and validation sets
val_dataset = dataset.take(len(filenames) // 5)
train_dataset = dataset.skip(len(filenames) // 5)

# Define the model
model = keras.Sequential(
    [
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu", input_shape=input_shape),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(128, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(256, kernel_size=(3, 3), activation="relu"),
        layers.Conv2D(256, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(512, kernel_size=(3, 3), activation="relu"),
        layers.Conv2D(512, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dense(4096, activation="relu"),
        layers.Dense(4096, activation="relu"),
        layers.Dense(num_art_epochs, activation="softmax"),
    ]
)

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

# Train the model
model.fit(
    train_dataset,
    epochs=num_art_epochs,
    validation_data=val_dataset,
    verbose=1,
)