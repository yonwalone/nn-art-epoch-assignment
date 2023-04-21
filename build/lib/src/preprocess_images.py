import os
import cv2
import numpy as np
import time
import shutil
from pathlib import Path
import matplotlib.pyplot as plt


class Preprocess_Images:
    """
    Pipeline for preprocessing images:
        1. Balancing
        2. Resizing
        3. Grayscaling
        4. Augmentation
        5. Normalisation
    """

    def __init__(
            self, 
            input_dir, 
            output_dir,
            balancing=2,
            target_size=256,
            grayscale = True, 
            augmentations=4,
            process_name="pre1",
            allowed_extensions = ["png", "jpg", "jpeg"]
            ):
        """Initialize the object's attributes.

        Args:
            input_dir (string): Path to input directory.
            output_dir (string): Path to output directory.
            balancing (int, optional): Number of individual images for each epoch. Defaults to 5000.
            target_size (int, optional): Target resolution of the images. Defaults to 256.
            grayscale (boolean, optional): Grayscaling as part of the pipeline. Defaults to True.
            augmentations (int, optional): Number of augmentations per image. Defaults to 4.
            process_image (string, optional): Name of the pipeline. Defaults to "pre1".
            allowed_extension (list, optional): List of strings containing exceptions. 
            Defaults to ["png", "jpg", "jpeg"].
        """

        self.input_dir = input_dir
        self.output_dir = output_dir
        self.balancing = balancing
        self.target_size = target_size
        self.grayscale = grayscale
        self.augmentations = augmentations
        self.process_name = process_name
        self.allowed_extensions = allowed_extensions

    
    def create_dir(self, path, set_output=False, set_input=False):
        """
        Create a new directory and set it as output_dir and input_dir of the instance if defined.

        Args:
            path (string): Path to the new directory.
            set_output (bool, optional): Defines if instances output_dir is updated. 
                Defaults to False.
            set_input (bool, optional): Defines if instances input_dir is updated. 
                Defaults to False.
        """
        Path(path).mkdir(parents=True, exist_ok=True)

        if set_output:
            self.output_dir = path

        if set_input:
            self.input_dir = path
    

    def move_images_by_epoch(self):
        """
        Move a specified number of images from the input direcory of the instance
        that start with the given epoch string to the output directory.

        Args:
            None

        Returns:
            None
        """
        input_dir = self.input_dir
        output_dir = self.output_dir
        balancing = self.balancing
        allowed_extensions = self.allowed_extensions

        # Create a dictionary to store the number of images to keep for each epoch
        number_to_keep_dict = {}

        for filename in os.listdir(input_dir):
            # Check if file extension is in the list of allowed extensions
            if any(filename.lower().endswith(ext) for ext in allowed_extensions):
                # Extract the epoch 
                epoch = filename.split("_")[0]

                # Set the number of images to keep for epoch
                if epoch not in number_to_keep_dict:
                    # If epoch appeared first timexx
                    number_to_keep_dict[epoch] = balancing
                else:
                    number_to_keep_dict[epoch] -= 1
                
                # Move the file if the limit is not yet reached
                if number_to_keep_dict[epoch] > 0:
                    image_path = os.path.join(input_dir, filename)
                    new_image_path = os.path.join(output_dir, filename)
                    shutil.move(image_path, new_image_path)
    

    def copy_images_by_epoch(self):
        """
        Copy a specified number of images from the input direcory of the instance
        that start with the given epoch string to the output directory.

        Args:
            None

        Returns:
            None
        """
        input_dir = self.input_dir
        output_dir = self.output_dir
        balancing = self.balancing
        allowed_extensions = self.allowed_extensions

        # Create a dictionary to store the number of images to keep for each epoch
        number_to_keep_dict = {}

        for filename in os.listdir(input_dir):
            # Check if file extension is in the list of allowed extensions
            if any(filename.lower().endswith(ext) for ext in allowed_extensions):
                # Extract the epoch 
                epoch = filename.split("_")[0]

                # Set the number of images to keep for epoch
                if epoch not in number_to_keep_dict:
                    # If epoch appeared first time
                    number_to_keep_dict[epoch] = balancing
                else:
                    number_to_keep_dict[epoch] -= 1
                
                # Copy the file if the limit is not yet reached
                if number_to_keep_dict[epoch] > 0:
                    image_path = os.path.join(input_dir, filename)
                    copied_image_path = os.path.join(output_dir, filename)
                    shutil.copy(image_path, copied_image_path)


    def delete_images_by_epoch(self):
        """
        Delete all images except a certain number of images for each epoch.

        Args:
            None

        Returns:
            None
        """
        input_dir = self.input_dir
        balancing = self.balancing
        allowed_extensions = self.allowed_extensions
        
        # Create a dictionary to store the number of images to keep for each epoch
        number_to_keep_dict = {}

        for filename in os.listdir(input_dir):
            # Check if file extension is in the list of allowed extensions
            if any(filename.lower().endswith(ext) for ext in allowed_extensions):
                # Extract the epoch 
                epoch = filename.split("_")[0]

                # Set the number of images to keep for epoch
                if epoch not in number_to_keep_dict:
                    # If epoch appeared first time
                    number_to_keep_dict[epoch] = balancing
                else:
                    number_to_keep_dict[epoch] -= 1
                
                # If number of images is exceeded delete the file
                if number_to_keep_dict[epoch] <= 0:
                    os.remove(os.path.join(input_dir, filename))
    

    def resize_images_affine(self):
        """
        Resize the image using an affine transformation matrix.

        Args:
            None
        """
        input_dir = self.input_dir
        output_dir = self.output_dir
        target_size = self.target_size
        allowed_extensions = self.allowed_extensions
        process_name = self.process_name

        image_size = (target_size, target_size)

        for filename in os.listdir(input_dir):
            # Check if file extension is in the list of allowed extensions
            if any(filename.lower().endswith(ext) for ext in allowed_extensions):
                image = cv2.imread(os.path.join(input_dir, filename))

                # Calculate the scaling factor to resize the image
                scale_x = image_size[0] / image.shape[1]
                scale_y = image_size[1] / image.shape[0]

                # Define the transformation matrix
                Matrix = np.array([[scale_x, 0, 0], [0, scale_y, 0]], dtype=np.float32)
                # Apply the affine transformation to the image
                resized_image = cv2.warpAffine(image, Matrix, image_size)

                # Generating a new filename and save the resized image
                epoch = filename.split('_')[0]
                extension = filename.split('.')[1]
                output_filename = f'{epoch}_{str(round(time.time()*1000))}_{process_name}_affin.{extension}'
                cv2.imwrite(os.path.join(output_dir, output_filename), resized_image)


    def resize_images_squared(self):
        """
        Resize the image to a square of the specified size by resizing the image
        and than cropp a centered square out of it.

        Args:
            None
        """
        input_dir = self.input_dir
        output_dir = self.output_dir
        target_size = self.target_size
        process_name = self.process_name
        allowed_extensions = self.allowed_extensions

        image_size = (target_size, target_size)

        for filename in os.listdir(input_dir):
            # Check if file extension is in the list of allowed extensions
            if any(filename.lower().endswith(ext) for ext in allowed_extensions):
                image = cv2.imread(os.path.join(input_dir, filename))

                # Get the dimensions of the input image
                height, width = image.shape[:2]
                # Find the smallest dimension of the image
                min_dimension = min(width, height)

                # Calculate the scale factor to fit the image inside the square
                scale = image_size[0] / min_dimension
                image = cv2.resize(image, (0, 0), fx=scale, fy=scale)

                # Calulate the center of the image
                center_x, center_y = image.shape[1] // 2, image.shape[0] // 2

                # Calculate the coordinates of the top-left and bottom-right corners of the square
                x1 = center_x - image_size[0] // 2
                y1 = center_y - image_size[1]  // 2
                x2 = x1 + image_size[0]
                y2 = y1 + image_size[1]

                # Crop the image to the square
                squared_image = image[y1:y2, x1:x2]

                # Generating a new filename and save the resized image
                epoch = filename.split('_')[0]
                extension = filename.split('.')[1]
                output_filename = f'{epoch}_{str(round(time.time()*1000))}_{process_name}_squared.{extension}'
                cv2.imwrite(os.path.join(output_dir, output_filename), squared_image)


    def grayscale_images(self):
        """
        Convert the given input images to grayscale.

        Args:
            None
        """
        input_dir = self.input_dir
        output_dir = self.output_dir
        process_name = self.process_name
        allowed_extensions = self.allowed_extensions

        for filename in os.listdir(input_dir):
            # Check if file extension is in the list of allowed extensions
            if any(filename.lower().endswith(ext) for ext in allowed_extensions):
                image = cv2.imread(os.path.join(input_dir, filename))

                # Transform image from BGR color space to gray
                grayed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # Generating a new filename and save the grayscaled image
                epoch = filename.split('_')[0]
                extension = filename.split('.')[1]
                output_filename = f'{epoch}_{str(round(time.time()*1000))}_{process_name}.{extension}'
                cv2.imwrite(os.path.join(output_dir, output_filename), grayed_image)


    def augment_images(self):
        """
        Augment the images in the input directory using OpenCV.

        Args:
            None
        """
        # Define the augmentations to apply
        augmentations = [
            ("fliph", cv2.flip, 1),
            ("flipv", cv2.flip, 0),
            ("rotate", self.rotate_image, None),
            ("blur", self.blur_image, None)
        ]

        for filename in os.listdir(self.input_dir):
            # Check if file extension is in the list of allowed extensions
            if any(filename.lower().endswith(ext) for ext in self.allowed_extensions):
                image = cv2.imread(os.path.join(self.input_dir, filename))

                # Apply the augmentations
                for i in range(self.augmentations):
                    # Choose a random augmentation
                    name, func, arg = augmentations[np.random.randint(0, len(augmentations))]

                    # Apply the augmentation
                    if arg is not None:
                        image = func(image, arg)
                    else:
                        image = func(image)

                    # Generating a new filename and save the augmented image
                    epoch = filename.split('_')[0]
                    extension = filename.split('.')[1]
                    output_filename = f'{epoch}_{str(round(time.time()*1000))}_{name}_{self.process_name}.{extension}'
                    cv2.imwrite(os.path.join(self.output_dir, output_filename), image)


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
        

    def normalize_images(self):
        """""
        Normalize images from a directory and save them in a NumPy array.

        Args:
            None       

        Returns:
            A NumPy array containing the normalized images.
        """""
        normalized_images = []

        for filename in os.listdir(self.input_dir):
            # Check if file extension is in the list of allowed extensions
            if any(filename.lower().endswith(ext) for ext in self.allowed_extensions):
                image = cv2.imread(os.path.join(self.input_dir, filename))

                # Normalize image and add to list.
                normalized_image = image / 255.
                normalized_images.append(normalized_image)

        # Convert the list of normalized images to a NumPy array
        normalized_images = np.array(normalized_images)

        if self.grayscale:
            # Take the mean of the pixel values across the color channels (axis 3)
            squeezed_images = np.mean(normalized_images, 3)
            return squeezed_images
        else:
            return normalized_images
    

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
