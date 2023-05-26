import os
import json
import numpy as np
import tensorflow as tf
from config import EPOCHS, PROJECT_ROOT
import src.model_helper as mh

mh.log("### Starting test pipeline ###")

model_name = "my_model"
model_file_name = f"{model_name}.h5"
model_creation_log = "log_first_model.txt"
used_prep_pipe = "3x224"
testing_files_per_epoch = 6400
batch_size = 32

DATA_PATH = os.path.join(PROJECT_ROOT, "data")
CACHE_PATH = os.path.join(DATA_PATH, "cache", model_name)
if not os.path.exists(CACHE_PATH):
    os.mkdir(CACHE_PATH)
model_path = os.path.join(PROJECT_ROOT, "results", model_file_name)
creation_log_path = os.path.join(DATA_PATH, "logs", model_creation_log)

used_files = mh.get_used_files_of_log(creation_log_path)

model = tf.keras.models.load_model(model_path)

usable_files = []
labels = []

for art_epoch in EPOCHS:
    image_path = os.path.join(DATA_PATH, art_epoch, "images", used_prep_pipe, "normalized")
    all_epoch_files = os.listdir(image_path)
    usable_files_of_epoch = list(filter(lambda x: x not in used_files, all_epoch_files))[:testing_files_per_epoch]
    np_labels = mh.one_hot_encode(art_epoch)
    usable_files.append(usable_files_of_epoch)
    labels.append([np_labels for _ in usable_files_of_epoch])

with open(os.path.join(CACHE_PATH, 'usable_files_{model_name}.json'), 'w') as f:
    json.dump(usable_files, f)

np.save(os.path.join(CACHE_PATH, 'labels_{model_name}.npy'), labels)

mh.log("Filenames and Labels saved!")



with open(os.path.join(CACHE_PATH,'usable_files_{model_name}.json'), 'r') as f:
    usable_files = json.load(f)

labels = np.load(os.path.join(CACHE_PATH, 'labels_{model_name}.npy'))

predictions = []

for index, art_epoch in enumerate(EPOCHS):
    mh.log(f"Now preparing data for epoch {art_epoch}")
    current_inputs = []
    for current_batch in range(len(usable_files[index])//batch_size):
        mh.log(f"Now testing batch {current_batch}", noprint=True)
        image_path=os.path.join(DATA_PATH, art_epoch, "images", used_prep_pipe, "normalized")
        start_index = current_batch * batch_size
        end_index = start_index + batch_size
        for image in usable_files[index][start_index:end_index]:
            mh.log(f'Used picture {image}', noprint=True)
            data = np.load(os.path.join(image_path, image))
            np_data = data[list(data.files)[0]]

            current_inputs.append(np_data)
    np_current_inputs = np.transpose(np.array(current_inputs), (0, 2, 3, 1))
    # Train the model
    print(f"Started testing model on epoch {art_epoch}")
    curr_predictions = model.predict(np_current_inputs)
    predictions.append(curr_predictions)


mh.log(predictions, noprint=True)
np_predictions = np.array(predictions)
np.save(os.path.join(CACHE_PATH, f'pred_labels_{model_name}.npy'), np_predictions)

np_predictions = np.load(os.path.join(CACHE_PATH, f'pred_labels_{model_name}.npy'))
predicted_labels = np.argmax(np_predictions, axis=2)
given_labels = np.argmax(labels, axis=2)

# Compare predicted labels with ground truth labels
correct_predictions = np.sum(np.equal(predicted_labels, given_labels))
total_predictions = np.size(given_labels)

# Calculate accuracy
accuracy = correct_predictions / total_predictions
mh.log("Accuracy: {:.2%} {}/{}".format(accuracy, correct_predictions, total_predictions))
mh.log("### Test pipeline finished ###")

