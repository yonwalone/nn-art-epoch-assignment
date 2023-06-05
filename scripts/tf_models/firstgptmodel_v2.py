import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers
from config import EPOCHS, PROJECT_ROOT
import src.model_helper as mh
import matplotlib.pyplot as plt
# Changed batch size and added augmentation on train_gen
# 08/208 - 45s - loss: 1.8166 - accuracy: 0.3426 - 45s/epoch - 217ms/step

using_split = "only_resized_all_epochs"
model_name = "inception_model_v2"
batch_size = 32
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
    batch_size=batch_size,
    shuffle=False,
    color_mode="rgb",
    classes=EPOCHS
)

items = os.listdir(os.path.join(SPLIT_PATH, "train"))
# Filter the list to include only folders
folders = [item for item in items if os.path.isdir(os.path.join(SPLIT_PATH, "train", item))]
# Get the count of epoch folders
art_epoch_count = len(folders)

# model_name = "first_gpt_model"
# model = keras.Sequential(
#     [
#         layers.Conv2D(32, kernel_size=(3, 3), activation="relu", input_shape=(224,224,3)),
#         layers.MaxPooling2D(pool_size=(2, 2)),
#         layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
#         layers.MaxPooling2D(pool_size=(2, 2)),
#         layers.Flatten(),
#         layers.Dense(128, activation="relu"),
#         layers.Dense(art_epoch_count, activation="softmax"),
#     ]
# )
def inception_module(prev_layer, filters):
    conv1 = layers.Conv2D(filters[0], kernel_size=(1, 1), activation="relu")(prev_layer)

    conv3 = layers.Conv2D(filters[1], kernel_size=(1, 1), activation="relu")(prev_layer)
    conv3 = layers.Conv2D(filters[2], kernel_size=(3, 3), padding="same", activation="relu")(conv3)

    conv5 = layers.Conv2D(filters[3], kernel_size=(1, 1), activation="relu")(prev_layer)
    conv5 = layers.Conv2D(filters[4], kernel_size=(5, 5), padding="same", activation="relu")(conv5)

    pool = layers.MaxPooling2D(pool_size=(3, 3), strides=(1, 1), padding="same")(prev_layer)
    pool = layers.Conv2D(filters[5], kernel_size=(1, 1), activation="relu")(pool)

    concat = layers.concatenate([conv1, conv3, conv5, pool], axis=-1)

    return concat

# Define your model using Inception module
input_shape = (224, 224, 3)
model = keras.Sequential(
    [
        layers.Conv2D(32, kernel_size=(3, 3), activation="relu", input_shape=input_shape),
        layers.MaxPooling2D(pool_size=(2, 2)),
        inception_module(model.layers[1].output, [64, 96, 128, 16, 32, 32]),
        inception_module(model.layers[2].output, [128, 128, 192, 32, 96, 64]),
        layers.Flatten(),
        layers.Dense(128, activation="relu"),
        layers.Dense(art_epoch_count, activation="softmax"),
    ]
)


print(model.summary())

optimizer = keras.optimizers.Adam()
loss = keras.losses.SparseCategoricalCrossentropy()
metrics = ["accuracy"]

model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

# Training

epochs = 20

early_stopping= keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=30,
    verbose=2
)

history = model.fit(train_batches, validation_data=valid_batches, 
                    callbacks=[early_stopping], epochs=epochs, verbose=1)


model.save(os.path.join(PROJECT_ROOT, "results", f"{model_name}.h5"))

plt.figure(figsize=(16, 6))
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='train loss')
plt.plot(history.history['val_loss'], label='valid loss')
plt.grid()
plt.legend(fontsize=15)
plt.show()
plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='train acc')
plt.plot(history.history['val_accuracy'], label='valid acc')
plt.grid()
plt.legend(fontsize=15)
plt.show()

model.evaluate(test_batches, verbose=2)