import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.utils import to_categorical
from config import EPOCHS, PROJECT_ROOT
import src.model_helper as mh
import matplotlib.pyplot as plt

DATA_PATH = os.path.join(PROJECT_ROOT, "data")

input_shape = (224, 224, 3)
num_art_epochs = min(4, len(EPOCHS))
batch_size = 32
train_epochs = 1
used_preprocess_pipeline = "3x224"
amount_total_img_per_epoch = 32000
train_end_index = int(amount_total_img_per_epoch * 0.8)
test_end_index = amount_total_img_per_epoch

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

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# Train the model
for train_epoch in range(train_epochs):
    mh.log(f"Started training of train_epoch {train_epoch}")
    for current_batch in range(train_end_index//batch_size):
        mh.log(f"Now training batch {current_batch}")
        x_batch_train = []
        y_batch_train = []
        for art_epoch in EPOCHS[:num_art_epochs]:
            mh.log(f"Preparing data for epoch {art_epoch}")
            np_labels = mh.one_hot_encode(art_epoch)
            image_path=os.path.join(DATA_PATH, art_epoch, "images", used_preprocess_pipeline, "normalized")
            start_index = current_batch * batch_size
            end_index = min(train_end_index - 1 ,start_index + batch_size)
            for image in os.listdir(image_path)[start_index:end_index]:
                mh.log(f'Used picture {image}', noprint=True)
                data = np.load(os.path.join(image_path, image))
                np_data = data[list(data.files)[0]]

                x_batch_train.append(np_data)
                y_batch_train.append(np_labels)

        x_batch_train = np.transpose(np.array(x_batch_train), (0, 2, 3, 1))
        y_batch_train = np.array(y_batch_train)
        
        # Train the model
        print(f"Started training model on batch {current_batch}")
        model.fit(x_batch_train, y_batch_train, epochs=1, shuffle=True)
        print(f"Finished training model on batch {current_batch}")

model.save(os.path.join(PROJECT_ROOT, "results", "my_model.h5"))
