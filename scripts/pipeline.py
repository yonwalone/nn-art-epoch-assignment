import os
from src.preprocess_images import Preprocess_Images


print("##### Started preprocess pipeline. #####")
print("-----   Installing own packages.   -----")
os.system("pip install -e .")

# Set folder path
folder_path = "/Users/SOK1USH/Documents/nn-art-epoch-assignment/data/"

# Creating a preproces instance
pre1 = Preprocess_Images(folder_path, folder_path, grayscale=False)

print(f"----- STARTED balancing to {pre1.balancing} images. -----")
pre1.create_dir(f"{folder_path}{pre1.process_name}/balancing/")
pre1.copy_images_by_epoch()
print(f"----- FINISHED balancing. -----")

print(f"----- STARTED resizing. -----")
pre1.input_dir = f"{folder_path}{pre1.process_name}/balancing/"
pre1.create_dir(f"{folder_path}{pre1.process_name}/resizing/")
pre1.resize_images_affine()
pre1.resize_images_squared()
print(f"----- FINISHED resizing. -----")

if pre1.grayscale:
    print(f"----- STARTED grayscaling. -----")
    pre1.input_dir = f"{folder_path}{pre1.process_name}/resizing/"
    pre1.create_dir(f"{folder_path}{pre1.process_name}/grayscaling/")
    pre1.grayscale_images()
    pre1.input_dir = f"{folder_path}{pre1.process_name}/grayscaling/"
    print(f"----- FINISHED grayscaling. -----")
else:
    print(f"----- NO grayscaling for {pre1.process_name} -----")
    pre1.input_dir = f"{folder_path}{pre1.process_name}/resizing/"

print(f"----- STARTED augmentation. -----")
pre1.create_dir(f"{folder_path}{pre1.process_name}/augmentation/")
pre1.augment_images()
print(f"----- FINISHED augmentation. -----")

print(f"----- STARTED normalisation. -----")
pre1.input_dir = f"{folder_path}{pre1.process_name}/augmentation/"
normalized_images = pre1.normalize_images()
print(f"----- FINISHED normalisation. -----")
# print(normalized_images[0])
# pre1.show_image(normalized_images[0])


