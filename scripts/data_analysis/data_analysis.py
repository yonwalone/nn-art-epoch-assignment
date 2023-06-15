# Was könnte man analysieren?
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
#from skimage.feature import greycomatrix

from config import EPOCHS, PROJECT_ROOT
from excel_export import exportToExcel, ColorMode
from functions import allcolorHistogram
from views import viewColorsHistogram

def getImages():
    """
    Get images from directory
    """
    using_split = "only_resized_all_epochs"
    folder_path = os.path.join(PROJECT_ROOT, "data", "splits", using_split, "train", "baroque")

    image_files = os.listdir(folder_path)

    images = []
    for file_name in image_files:
        if file_name.endswith(".jpg") or file_name.endswith(".png"):
            image_path = os.path.join(folder_path, file_name)
            image = cv2.imread(image_path)
            images.append(image)

    return images

images = getImages()
#images = [cv2.imread("test_image.jpg")]
#plotManyImages(images)

plt.close()

epoch = "baroque"

colList, bins = allcolorHistogram(images)
viewColorsHistogram(colList, bins)


plt.close()
exit()

# Calculate values 
colors = calculateColorAverages(images) # Achtung Reihenfolge ist nicht RGB!
contrasts = calculateContrast(images)
edgeCounts = extractEdges(images)
outLine = [epoch] + colors + contrasts + edgeCounts

print(outLine)

# Prepare Output
columns = ["Epoch",
           "Avg Color", "Avg Color Red", "Avg Color Green", "Avg Color Blue",
           "Std Color", "Std Color Red", "Std Color Green", "Std Color Blue",
           "Avg Contrast", "Avg Contrast Red", "Avg Contrast Green", "Avg Contrast Blue",
           "Std Contrast", "Std Contrast Red", "Std Contrast Green", "Std Contrast Blue",
           "Avg Edge Count", "Std Edge Count"
           ]

outLines = [outLine]
exportToExcel(columNames=columns, data=outLines, filename="analysis.xlsx")

plt.close()