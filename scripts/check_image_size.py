import os
import cv2
import json
from config import EPOCHS, PROJECT_ROOT

DATA_PATH = os.path.join(PROJECT_ROOT, "data")
expectedSize = 300
image_counts = {}

for art_epoch in EPOCHS:
    images_path = os.path.join(DATA_PATH, art_epoch, "images")
    all_files = os.listdir(images_path)
    image_counts[art_epoch] = 0

    for imageIndex, imageName in enumerate(all_files):
        if not imageName.endswith(".jpg"):
            continue

        try:
            img = cv2.imread(os.path.join(images_path, imageName))
            if img is None or img.shape[0] < expectedSize or img.shape[1] < expectedSize:
                continue
        except:
            continue

        count = image_counts[art_epoch]
        count += 1
        image_counts[art_epoch] = count

json_file_path = os.path.join(PROJECT_ROOT, "results", "image_counts.json")
with open(json_file_path, "w") as json_file:
    json.dump(image_counts, json_file)

print("Image counts saved to:", json_file_path)







