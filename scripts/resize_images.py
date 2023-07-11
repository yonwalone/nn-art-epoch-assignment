import os
import cv2
import numpy as np
from config import EPOCHS, PROJECT_ROOT

txt_file_path = os.path.join(PROJECT_ROOT, "results", "valid_image_paths.txt")
output_dir = os.path.join(PROJECT_ROOT, "data", "3x384")

TARGET_SIZE = 384

os.makedirs(output_dir, exist_ok=True)

# Read the image paths from the text file
image_paths = []
with open(txt_file_path, "r") as txt_file:
    for line in txt_file:
        image_path = line.strip()  # Remove leading/trailing whitespace and newline character
        image_paths.append(image_path)

# Process each image
for image_path in image_paths:
    # Extract the art epoch from the image path
    art_epoch = image_path.split("/")[-2]

    epoch_folder = os.path.join(output_dir, art_epoch)
    os.makedirs(epoch_folder, exist_ok=True)

    # Resize the image
    resized_image = affine_resize(image_path=image_path)

    # Get the filename of the resized image
    image_filename = os.path.basename(image_path)
    resized_image_path = os.path.join(epoch_folder, image_filename)

    # Save the resized image
    cv2.imwrite(resized_image_path, resized_image)

    print("Resized image saved:", resized_image_path)
