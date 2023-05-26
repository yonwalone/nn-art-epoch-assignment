import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from config import EPOCHS, PROJECT_ROOT
import src.model_helper as mh
import matplotlib.pyplot as plt

using_split = "fully_augmented_all_epochs"
batch_size = 4
SPLIT_PATH = os.path.join(PROJECT_ROOT, "data", "splits", using_split)

train_gen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
valid_gen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
test_gen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)

train_batches = train_gen.flow_from_directory(
    os.path.join(SPLIT_PATH, "train"),
    target_size=(224, 224),
    class_mode="sparse",
    batch_size=batch_size,
    shuffle=True,
    color_mode="rgb",
    classes=EPOCHS
)

valid_batches = train_gen.flow_from_directory(
    os.path.join(SPLIT_PATH, "valid"),
    target_size=(224, 224),
    class_mode="sparse",
    batch_size=batch_size,
    shuffle=False,
    color_mode="rgb",
    classes=EPOCHS
)

test_batches = train_gen.flow_from_directory(
    os.path.join(SPLIT_PATH, "test"),
    target_size=(224, 224),
    class_mode="sparse",
    batch_size=batch_size,
    shuffle=False,
    color_mode="rgb",
    classes=EPOCHS
)

model = tf.keras.applications.inception_v3.InceptionV3()
print(model.summary())

optimizer = keras.optimizers.Adam()
loss = keras.losses.SparseCategoricalCrossentropy()
metrics = ["accuracy"]

model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

# Training

epochs = 30

early_stopping= keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=30,
    verbose=2
)

history = model.fit(train_batches, validation_data=valid_batches, 
                    callbacks=[early_stopping], epochs=epochs, verbose=2)

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