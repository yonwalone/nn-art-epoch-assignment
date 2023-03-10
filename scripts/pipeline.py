import os
from src.preprocess_images import Preprocess_Images


print("##### Started preprocess pipeline. #####")
print("-----   Installing own packages.   -----")
os.system("pip install -e .")

folder_path = "/Users/SOK1USH/Documents/nn-art-epoch-assignment/data/"

pre1 = Preprocess_Images(folder_path, folder_path, grayscale=True)

print(f"----- STARTED balancing to {pre1.balancing} images. -----")
balancing_path = f"{folder_path}{pre1.process_name}/balancing/"
pre1.create_dir(balancing_path, set_output=True)
pre1.copy_images_by_epoch()
pre1.input_dir = balancing_path
print(f"----- FINISHED balancing. -----")

print(f"----- STARTED resizing. -----")
resizing_path = f"{folder_path}{pre1.process_name}/resizing/"
pre1.create_dir(resizing_path, set_output=True)
pre1.resize_images_affine()
pre1.resize_images_squared()
pre1.input_dir = resizing_path
print(f"----- FINISHED resizing. -----")

# Optional grayscaling if set to True
if pre1.grayscale:
    print(f"----- STARTED grayscaling. -----")
    grayscale_path = f"{folder_path}{pre1.process_name}/grayscaling/"
    pre1.create_dir(grayscale_path, set_output=True)
    pre1.grayscale_images()
    pre1.input_dir = grayscale_path
    print(f"----- FINISHED grayscaling. -----")

print(f"----- STARTED augmentation. -----")
augmentation_path = f"{folder_path}{pre1.process_name}/augmentation/"
pre1.create_dir(augmentation_path, set_output=True)
pre1.augment_images()
pre1.input_dir = augmentation_path
print(f"----- FINISHED augmentation. -----")

print(f"----- STARTED normalisation. -----")
pre1.input_dir = f"{folder_path}{pre1.process_name}/augmentation/"
normalized_images = pre1.normalize_images()
print(f"----- FINISHED normalisation. -----")
