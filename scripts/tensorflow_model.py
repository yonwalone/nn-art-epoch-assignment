
import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.utils import to_categorical
from config import EPOCHS, PROJECT_ROOT
import src.model_helper as mh


if __name__ == "__main__":
    DATA_PATH = os.path.join(PROJECT_ROOT, "data")

    input_shape = (224, 224, 3)
    num_art_epochs = min(10, len(EPOCHS))
    batch_size = 32
    train_epochs = 2
    used_preprocess_pipeline = "3x224"
    amount_total_img_per_epoch = 2560
    train_end_index = int(2500 * 0.8)
    test_end_index = amount_total_img_per_epoch

    # Create a list of filenames and labels for all images
    filenames = []
    labels = []
    current_batch = 0


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


    for train_epoch in range(train_epochs):
        mh.log(f"Started training of train_epoch {train_epoch}")
        for current_batch in range(train_end_index//batch_size):
            mh.log(f"Now training batch {current_batch}")
            x_batch_train = []
            y_batch_train = []
            for art_epoch in EPOCHS[:num_art_epochs]:
                mh.log(f"Training art_epoch {art_epoch}")
                np_labels = mh.one_hot_encode(art_epoch)
                image_path=os.path.join(DATA_PATH, art_epoch, "images", used_preprocess_pipeline, "normalized")
                start_index = current_batch * batch_size
                end_index = min(train_end_index - 1 ,start_index + batch_size)
                for image in os.listdir(image_path)[start_index:end_index]:
                    data = np.load(os.path.join(image_path, image))
                    x_batch_train.append(data)
                    y_batch_train.append(np_labels)
        model.train_on_batch(x_batch_train, y_batch_train)


    # model.fit(
    #     train_dataset,
    #     epochs=num_art_epochs,
    #     validation_data=val_dataset,
    #     verbose=1,
    # )
