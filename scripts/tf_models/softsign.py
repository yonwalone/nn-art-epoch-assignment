import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers
from config import EPOCHS, PROJECT_ROOT
import src.model_helper as mh
import matplotlib.pyplot as plt

using_split = "only_resized_all_epochs"
model_name = "five_staples_softsign"
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
    batch_size=batch_size,
    shuffle=False,
    color_mode="rgb",
    classes=EPOCHS
)

# Create model

model = keras.Sequential(
    [
        layers.Conv2D(32, kernel_size=(3, 3), activation="softsign", input_shape=(224,224,3)),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(3, 3), activation="softsign"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(3, 3), activation="softsign"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(3, 3), activation="softsign"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(3, 3), activation="softsign"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation="softsign"),
        layers.Dense(10, activation="softmax"),
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

# Test
model.evaluate(test_batches, verbose=1)

# Print statistics
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