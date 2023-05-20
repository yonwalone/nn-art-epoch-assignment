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
num_art_epochs = min(10, len(EPOCHS))
batch_size = 32
train_epochs = 2
used_preprocess_pipeline = "3x224"
amount_total_img_per_epoch = 2560
train_end_index = int(2500 * 0.8)
test_end_index = amount_total_img_per_epoch

# model = keras.Sequential(
#     [
#         layers.Conv2D(64, kernel_size=(3, 3), activation="relu", input_shape=input_shape),
#         layers.MaxPooling2D(pool_size=(2, 2)),
#         layers.Conv2D(128, kernel_size=(3, 3), activation="relu"),
#         layers.MaxPooling2D(pool_size=(2, 2)),
#         layers.Conv2D(256, kernel_size=(3, 3), activation="relu"),
#         layers.Conv2D(256, kernel_size=(3, 3), activation="relu"),
#         layers.MaxPooling2D(pool_size=(2, 2)),
#         layers.Conv2D(512, kernel_size=(3, 3), activation="relu"),
#         layers.Conv2D(512, kernel_size=(3, 3), activation="relu"),
#         layers.MaxPooling2D(pool_size=(2, 2)),
#         layers.Flatten(),
#         layers.Dense(4096, activation="relu"),
#         layers.Dense(4096, activation="relu"),
#         layers.Dense(num_art_epochs, activation="softmax"),
#     ]
# )

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))


model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

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
                data = np.load(os.path.join(image_path, image))
                np_data = data[list(data.files)[0]]

                x_batch_train.append(data)
                y_batch_train.append(np_labels)

        x_batch_train = np.array(x_batch_train)
        plt.imshow(x_batch_train[0])
        plt.axis('off')  # Turn off axis labels
        plt.show()
        y_batch_train = np.array(y_batch_train)
        
        # Train the model
        print(f"Started training model on batch {current_batch}")
        model.fit(x_batch_train, y_batch_train, batch_size, epochs=train_epochs)
        print(f"Finished training model on batch {current_batch}")

model.save(os.path.join(PROJECT_ROOT, "results", "my_model.h5"))
