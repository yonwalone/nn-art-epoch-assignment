# Was könnte man analysieren?
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os

from config import EPOCHS, PROJECT_ROOT
from color_mode import ColorMode
from functions import allcolorHistogram, calculateColorAverages, calculateContrast, extractEdges, calculateGreyCoMatrixMetrics, exportToExcel
from views import viewColorsHistogram, viewAllHistogram

def getEpochImages(epoch):
    """
    Get images of an epoch from train, valid and test

    Args:
    epoch (string): Name of epoch

    Returns:
    images (Array Images): found images
    """
    using_split = "only_resized_all_epochs"

    train_path = os.path.join(PROJECT_ROOT, "data", "splits", using_split, "train", epoch)
    train_files = os.listdir(train_path)

    valid_path = os.path.join(PROJECT_ROOT, "data", "splits", using_split, "valid", epoch)
    valid_files = os.listdir(valid_path)

    test_path = os.path.join(PROJECT_ROOT, "data", "splits", using_split, "test", epoch)
    test_files = os.listdir(test_path)

    images = []
    for file_name in train_files:
        if file_name.endswith(".jpg") or file_name.endswith(".png"):
            image_path = os.path.join(train_path, file_name)
            image = cv2.imread(image_path)
            images.append(image)

    for file_name in valid_files:
        if file_name.endswith(".jpg") or file_name.endswith(".png"):
            image_path = os.path.join(valid_path, file_name)
            image = cv2.imread(image_path)
            images.append(image)

    for file_name in test_files:
        if file_name.endswith(".jpg") or file_name.endswith(".png"):
            image_path = os.path.join(test_path, file_name)
            image = cv2.imread(image_path)
            images.append(image)

    return images

plt.close()

outLines=[]
allCols = []
allBins = []

for epoch in EPOCHS:
    # Tet images of epoch
    images = getEpochImages(epoch)

    # Calculate values for diagram
    colList, bins = allcolorHistogram(images)
    allCols.append(colList)
    allBins.append(bins)

    # Calculate metrics 
    colors = calculateColorAverages(images)
    contrasts = calculateContrast(images)
    edgeCounts = extractEdges(images)
    coMatrixMetrics = calculateGreyCoMatrixMetrics(images)

    outLine = [epoch] + colors + contrasts + edgeCounts + coMatrixMetrics
    outLines.append(outLine)

viewAllHistogram(allCols, allBins)

# Prepare Output
columns = ["Epoch",
           "Avg Color", "Avg Color Red", "Avg Color Green", "Avg Color Blue",
           "Std Color", "Std Color Red", "Std Color Green", "Std Color Blue",
           "Avg Contrast", "Avg Contrast Red", "Avg Contrast Green", "Avg Contrast Blue",
           "Std Contrast", "Std Contrast Red", "Std Contrast Green", "Std Contrast Blue",
           "Avg Edge Count", "Std Edge Count",
           "Avg Gray Contrast", "Std Gray Contrast",
           "Avg Dissimilarity", "Std Dissimilarity",
           "Avg Homogeneity", "Std Homogeneity",
           "Avg Energy", "Std Energy",
           "Avg Correlation", "Std Correlation"
           ]

exportToExcel(columNames=columns, data=outLines, fileName="analysis.xlsx")

plt.close()