import os
import cv2
import numpy as np
import shutil
from pathlib import Path
import matplotlib.pyplot as plt
from config import PROJECT_ROOT


DATA_PATH = os.path.join(PROJECT_ROOT, "data",)

class Preprocess_Images:
    """
    Pipeline for preprocessing images:
        1. Resizing
        2. Grayscaling
        3. Augmentation
        4. Normalisation
    """

    def __init__(
            self, 
            epoch,
            target_size=384,
            grayscale = True, 
            augmentations=4,
            process_name="pre1",
            allowed_extensions = [".png", ".jpg", ".jpeg"]
            ):
        """Initialize the object's attributes.

        Args:
            input_dir (string): Path to input directory.
            output_dir (string): Path to output directory.
            target_size (int, optional): Target resolution of the images. Defaults to 256.
            grayscale (boolean, optional): Grayscaling as part of the pipeline. Defaults to True.
            augmentations (int, optional): Number of augmentations per image. Defaults to 4.
            process_image (string, optional): Name of the pipeline. Defaults to "pre1".
            allowed_extension (list, optional): List of strings containing exceptions. 
            Defaults to ["png", "jpg", "jpeg"].
        """

        self.epoch = epoch
        self.target_size = target_size
        self.grayscale = grayscale
        self.augmentations = augmentations
        self.process_name = process_name
        self.allowed_extensions = allowed_extensions
        self.images_folder = os.path.join(DATA_PATH, self.epoch, "images", self.process_name)
    

        Path(self.images_folder).mkdir(parents=True,exist_ok=True)



    def create_dir(self, path):
        """
        Create a new directory and set it as output_dir and input_dir of the instance if defined.
        Args:
            path (string): Path to the new directory.
        """
        Path(path).mkdir(parents=True, exist_ok=True)

    def log(self, info, noprint=False):
        """
        Prints out the info and saves it in the log_file

        Args:
            info (string): The info which should be printed and logged.
        """
        info = str(info)
        if not noprint:
            print(info)

        log_file_path = os.path.join(self.images_folder, "01log.txt")
        with open(log_file_path, 'a') as log_file:
            log_file.write(info + "\n")

    def print_progress_bar(self, amount, of, start_text = "Progress", end_text = "", new_line = True):
        amount += 1
        progress = int(((amount)/of)*100)
        progress_bar = f"{start_text}: [{'='*int(progress/2)}{' '*(50-int(progress/2))}] {progress}% ({amount}/{of}) {end_text}"
        print(progress_bar, end="\r" if not new_line and progress < 100 else "\n")

    def get_files_by_size(self, input_dir, output_dir, min_size):
        """
        Copy images with a size above min size from input to output directory

        Args:
            input_dir (string): Foldername input
            output_dir (string): Foldername output
            min_size (int): Size a image should have
        """
        input_dir = os.path.join(self.images_folder, input_dir) if input_dir != "" else os.path.dirname(self.images_folder)
        output_dir = os.path.join(self.images_folder, output_dir)
        
        self.create_dir(output_dir)

        for index, filename in enumerate(os.listdir(input_dir)):
            if not filename.endswith(".jpg"):
                info=f"Unsupported extension: {filename}"
                self.print_progress_bar(index, len(os.listdir(input_dir)), start_text="Spliting files", end_text=info, new_line=False)
                continue

            try:
                img = cv2.imread(os.path.join(input_dir, filename))
                if img is None or img.shape[0] < min_size or img.shape[1] < min_size:
                    info=f"Too small: {filename}"
                    self.print_progress_bar(index, len(os.listdir(input_dir)), start_text="Spliting files", end_text=info, new_line=False)
                    continue
            except:
                info=f"Undefined error: {filename}"
                self.print_progress_bar(index, len(os.listdir(input_dir)), start_text="Spliting files", end_text=info, new_line=False)
                continue
            
            shutil.copy(os.path.join(input_dir, filename), os.path.join(output_dir, filename))
            info=f"success: {filename}"

            self.print_progress_bar(index, len(os.listdir(input_dir)), start_text="Spliting files", end_text=info, new_line=False)


    
    def resize_images_affine(self, input_dir, output_dir):
        """
        Resize the image using an affine transformation matrix.

        Args:
            input_dir (string): Foldername input
            output_dir (string): Foldername output
        """
        input_dir = os.path.join(self.images_folder, input_dir) if input_dir != "" else os.path.dirname(self.images_folder)
        output_dir = os.path.join(self.images_folder, output_dir)
        target_size = self.target_size

        self.create_dir(output_dir)

        for index, filename in enumerate(os.listdir(input_dir)):
            # Check if file extension is in the list of allowed extensions
            try:
                if os.path.splitext(filename)[1] in self.allowed_extensions:
                    image = cv2.imread(os.path.join(input_dir, filename))

                    # Calculate the scaling factor to resize the image
                    scale_x = target_size / image.shape[1]
                    scale_y = target_size / image.shape[0]

                    # Define the transformation matrix
                    matrix = np.array([[scale_x, 0, 0], [0, scale_y, 0]], dtype=np.float32)
                    # Apply the affine transformation to the image
                    resized_image = cv2.warpAffine(image, matrix, (target_size, target_size))

                    # Generating a new filename and save the resized image
                    extension = os.path.splitext(filename)[1]
                    filename = os.path.splitext(filename)[0]
                    output_filename = f'{filename}_affin{extension}'
                    cv2.imwrite(os.path.join(output_dir, output_filename), resized_image)
                    info = f"Success"
            except Exception as e:
                info = f"Failed"
                self.log(info, noprint=True)
            self.print_progress_bar(index, len(os.listdir(input_dir)), start_text="Affine resizing", end_text=info, new_line=False)
            

    def grayscale_images(self, input_dir, output_dir):
        """
        Convert the given input images to grayscale.

        Args:
            input_dir (string): Foldername input
            output_dir (string): Foldername output
        """
        input_dir = os.path.join(self.images_folder, input_dir)
        output_dir = os.path.join(self.images_folder, output_dir)
        
        self.create_dir(output_dir)

        for index, filename in enumerate(os.listdir(input_dir)):
            # Check if file extension is in the list of allowed extensions
            if os.path.splitext(filename)[1] in self.allowed_extensions:
                image = cv2.imread(os.path.join(input_dir, filename))

                # Transform image from BGR color space to gray
                grayed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # Generating a new filename and save the grayscaled image
                extension = os.path.splitext(filename)[1]
                filename = os.path.splitext(filename)[0]
                output_filename = f'{filename}_grayscale{extension}'
                cv2.imwrite(os.path.join(output_dir, output_filename), grayed_image)
                info=f"Success"
            else:
                info=f"Failed"
            self.print_progress_bar(index, len(os.listdir(input_dir)), start_text="Grayscaling", end_text=info, new_line=False)


    def augment_images(self, input_dir, output_dir):
        """
        Augment images from input directory and save them into output directory.

        Args:
            input_dir (string): Foldername input
            output_dir (string): Foldername output
        """
        input_dir = os.path.join(self.images_folder, input_dir)
        output_dir = os.path.join(self.images_folder, output_dir)

        self.create_dir(output_dir)

        # Define the augmentations to apply
        augmentations = [
            ("fliph", cv2.flip, 1),
            ("flipv", cv2.flip, 0),
            ("rotate", self.rotate_image, None),
            ("blur", self.blur_image, None)
        ]

        for index, filename in enumerate(os.listdir(input_dir)):
            # Check if file extension is in the list of allowed extensions
            if os.path.splitext(filename)[1] in self.allowed_extensions:
                image = cv2.imread(os.path.join(input_dir, filename))

                # Apply the augmentations
                for i in range(min(len(augmentations), self.augmentations)):
                    # Choose a random augmentation
                    name, func, arg = augmentations[i]

                    # Apply the augmentation
                    if arg is not None:
                        newImage = func(image, arg)
                    else:
                        newImage = func(image)

                    # Generating a new filename and save the augmented image
                    extension = os.path.splitext(filename)[1]
                    onlyfilename = os.path.splitext(filename)[0]
                    output_filename = f'{onlyfilename}_augmented_{name}{extension}'
                    try:
                        cv2.imwrite(os.path.join(output_dir, output_filename), newImage)
                        info=f"Success"
                    except Exception as e:
                        info=f"Failed"
                        
            else:
                info=f"Ext.fail"

            self.print_progress_bar(index, len(os.listdir(input_dir)), start_text="Augmentation", end_text=info, new_line=False)


    def rotate_image(self, image):
        """
        Rotate an image using a rotation matrix.

        Args:
            image (object): Cv2 image object.

        Returns:
            image: Cv2 image object.
        """
        angle = np.random.choice([-90, 90, 180])
        # Get the dimensions of the input image
        height, width = image.shape[:2]
        # Define the rotation matrix
        M = cv2.getRotationMatrix2D((width // 2, height // 2), angle, 1)
        # Apply the rotation to the image
        rotated_image = cv2.warpAffine(image, M, (width, height))

        return rotated_image
    

    def blur_image(self, image):
        """
        Blur an image using a Gaussian filter.

        Args:
            image (object): Cv2 image object.

        Returns:
            image: Cv2 image object
        """
        # Randomly choose a kernal size from a rang of values (3,5,7,9 or 11)
        kernel_size = np.random.choice(range(3, 12, 2))
        # The kernel size determines the Gaussian filter used to blue the image.
        blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

        return blurred_image
        

    def normalize_images(self, input_dir, output_dir):
        """
        Normalize images from a directory and save them in a NumPy array.

        Args:
            input_dir (string): Foldername input
            output_dir (string): Foldername output
        """
        input_dir = os.path.join(self.images_folder, input_dir)
        output_dir = os.path.join(self.images_folder, output_dir)

        self.create_dir(output_dir)

        for index, filename in enumerate(os.listdir(input_dir)):
            # Check if file extension is in the list of allowed extensions
            if os.path.splitext(filename)[1] in self.allowed_extensions:
                image = cv2.imread(os.path.join(input_dir, filename))

                processed_image = image / 255

                if self.grayscale:
                    processed_image = np.mean(processed_image, 3)

                transposed_image = processed_image.transpose((2, 0, 1))

                np.savez_compressed(f'{os.path.join(output_dir, os.path.splitext(filename)[0])}.npz', transposed_image)
                info=f"Success"
            else:
                info=f"Failed"

            self.print_progress_bar(index, len(os.listdir(input_dir)), start_text="Normalization", end_text=info, new_line=False)

    

    def show_image(self, image):
        """
        Display a single image using matplotlib.

        Args:
            self (object): Instance of the class.  

        Args:
            image: A NumPy array of an image.
        """
        plt.imshow(image)
        plt.axis('off')
        plt.show()
