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
model_name = "gpt_model_v2"
batch_size = 32
input_size = 224
SPLIT_PATH = os.path.join(PROJECT_ROOT, "data", "splits", using_split)


train_data= pd.read_csv(os.path.join(SPLIT_PATH, "train", "dataframe.csv"), sep="|")
#train_data["labels"]=train_data["labels"].apply(lambda x:x.replace("[",""))
#train_data["labels"]=train_data["labels"].apply(lambda x:x.replace("]",""))
#train_data["labels"]=train_data["labels"].apply(lambda x:x.split(","))

valid_data= pd.read_csv(os.path.join(SPLIT_PATH, "valid", "dataframe.csv"), sep="|")

test_data= pd.read_csv(os.path.join(SPLIT_PATH, "test", "dataframe.csv"), sep="|")


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
    dataframe=train_data,
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
    dataframe=valid_data,
    directory=os.path.join(os.path.join(SPLIT_PATH, "valid")),
    target_size=(input_size, input_size),
    class_mode="categorical",
    batch_size=batch_size,
    x_col="filename",
    y_col="labels",
    classes=EPOCHS
)

test_batches = test_gen.flow_from_dataframe(
    dataframe=test_data,
    directory=os.path.join(os.path.join(SPLIT_PATH, "test")),
    target_size=(input_size, input_size),
    class_mode="categorical",
    batch_size=batch_size,
    x_col="filename",
    y_col="labels",
    classes=EPOCHS
)

items = os.listdir(os.path.join(SPLIT_PATH, "train"))
# Filter the list to include only folders
folders = [item for item in items if os.path.isdir(os.path.join(SPLIT_PATH, "train", item))]
# Get the count of epoch folders
art_epoch_count = len(folders)

# model_name = "first_gpt_model"
model = keras.Sequential(
    [
        layers.Conv2D(32, kernel_size=(3, 3), activation="relu", input_shape=(224,224,3)),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation="relu"),
        layers.Dense(art_epoch_count, activation="sigmoid"),
    ]
)

print(model.summary())

optimizer = keras.optimizers.RMSprop(learning_rate=0.0001, weight_decay=1e-6)
loss = keras.losses.BinaryCrossentropy()
metrics = ["accuracy"]

model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

# Training

epochs = 1

#history = model.fit_generator(
#    generator=train_batches,
#    validation_data=valid_batches,
#    epochs=epochs
#)

history = model.fit(train_batches, validation_data= valid_batches, epochs=epochs, verbose=1)


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

#model.evaluate(test_batches, verbose=2)