import os
import numpy as np

from config import EPOCHS, PROJECT_ROOT
DATA_PATH = os.path.join(PROJECT_ROOT, 'data')


def load_image(filename):
    """
    Load and preprocess a single image

    Args:
        filename (string): filename of stored image
        label (string): label as string

    Returns:
        _type_: _description_
    """
    image = np.load(filename)["image"]
    labels = one_hot_encode(filename)

    return image, labels


def one_hot_encode(epoch_name):
    """
    TODO: Description

    Args:
        filename (_type_): _description_

    Returns:
        _type_: _description_
    """
    labels = [1 if epoch == epoch_name else 0 for epoch in EPOCHS]
    np_labels = np.array(labels)

    return np_labels
        