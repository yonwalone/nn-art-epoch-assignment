import os
from src.preprocess_images import Preprocess_Images
from config import PROJECT_ROOT, EPOCHS


def preprocess_epoch(epoch):
    print("##### Started preprocess pipeline. #####")

    pro_img = Preprocess_Images(
        epoch,
        grayscale=False, 
        process_name="3x224"
    )

    print(f"----- STARTED resizing. -----")
    pro_img.resize_images_affine(input_dir="", output_dir="resized")
    print(f"----- FINISHED resizing. -----")

    if pro_img.grayscale:
        print(f"----- STARTED grayscaling. -----")
        pro_img.grayscale_images(input_dir="resized", output_dir="grayscaled")
        print(f"----- FINISHED grayscaling. -----")

    print(f"----- STARTED augmentation. -----")
    pro_img.augment_images(input_dir="grayscaled" if pro_img.grayscale else "resized", output_dir="augmented")
    print(f"----- FINISHED augmentation. -----")

    print(f"----- STARTED normalisation. -----")
    pro_img.normalize_images(input_dir="augmented", output_dir="normalized")
    print(f"----- FINISHED normalisation. -----")


for epoch in EPOCHS:
    print(f"Hello, I'm now processing the images of the epoch {epoch}")
    preprocess_epoch(epoch)
    print(f"Bye, I have now processed the images of the epoch {epoch}")
