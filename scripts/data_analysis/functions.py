import numpy as np
import matplotlib.pyplot as plt
import cv2
from skimage import data
from skimage.feature import graycomatrix, graycoprops
from openpyxl import Workbook

from color_mode import ColorMode

def getAverage(image):
    """
    Calculate average values of image

    Args:
    image (NumPy Array): values representing image

    Returns:
    absAvg (number): average
    channelAvg (array of number): average of each channel
    """
    absAvg = np.mean(image)
    channelAvg = np.mean(image, axis=(0, 1))
    return absAvg, channelAvg


def getStd(image):
    """
    Calculate standard variation values of image

    Args:
    image (NumPy Array): values representing image

    Returns:
    allStd (number): standard derivaton
    channelStd (array of number): standard derovation of each channel
    """
    allStd = np.std(image)
    channelStd = np.std(image, axis=(0, 1))
    return allStd, channelStd


def calculateColorAverages(images):
    """
    Calculate information about the use of color in the images

    Args:
    image (List of NumPy Array): List of values representing an image

    Returns:
    (Array of numbers): color values of image
    """
    imgAverages = np.empty((0,))
    redAverages = np.empty((0,))
    greenAverages = np.empty((0,))
    blueAverages = np.empty((0,))

    for imageInd in range(0, len(images)):
        image = images[imageInd]
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        avg, channelAvg = getAverage(image_rgb)
        imgAverages = np.append(imgAverages, [avg])
        redAverages = np.append(redAverages, [channelAvg[0]])
        greenAverages = np.append(greenAverages, [channelAvg[1]])
        blueAverages = np.append(blueAverages, [channelAvg[2]])

    # Average values of the averge colors over the images
    imgAvgAvg = np.mean(imgAverages)
    redAvgAvg = np.mean(redAverages)
    greenAvgAvg = np.mean(greenAverages)
    blueAvgAvg = np.mean(blueAverages)

    # Std of the average colors over the images
    totalAvgStd = np.std(imgAverages)
    redAvgStd = np.std(redAverages)
    greenAvgStd = np.std(greenAverages)
    blueAvgStd = np.std(blueAverages)
    
    return [imgAvgAvg, redAvgAvg, greenAvgAvg, blueAvgAvg, totalAvgStd, redAvgStd, greenAvgStd, blueAvgStd]


def calculateContrast(images):
    """
    Calculate information about the contrast in the images

    Args:
    image (List of NumPy Array): List of values representing an image

    Returns:
    (Array of numbers): contrast values of image
    """
    imgStds = np.empty((0,))
    redStds = np.empty((0,))
    greenStds = np.empty((0,))
    blueStds = np.empty((0,))

    for imageInd in range(0, len(images)):
        image = images[imageInd]
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        std, channelStd = getStd(image_rgb)
        imgStds = np.append(imgStds, [std])
        redStds = np.append(redStds, [channelStd[0]])
        greenStds = np.append(greenStds, [channelStd[1]])
        blueStds = np.append(blueStds, [channelStd[2]])

    # Average values of the contrasts over the images
    imgStdAvg = np.mean(imgStds)
    redStdAvg = np.mean(redStds)
    greenStdAvg = np.mean(greenStds)
    blueStdAvg = np.mean(blueStds)

    # Std of the contrasts over the images
    imgStdStd = np.std(imgStds)
    redStdStd = np.std(redStds)
    greenStdStd = np.std(greenStds)
    blueStdStd = np.std(blueStds)
    
    return [imgStdAvg, redStdAvg, greenStdAvg, blueStdAvg, imgStdStd, redStdStd, greenStdStd, blueStdStd]


def extractEdges(images, showChart = False):
    """
    Extract Edges and recieve indicator for count of edges

    Args:
    image (List of NumPy Array): List of values representing an image
    showChart (Bool): should chart be drawn

    Returns:
    (Array of numbers): information about detected edges
    """
    edgeCounts = np.empty((0,))
    for imageInd in range(0, len(images)):
        image = images[imageInd]
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        grayImg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #edges = cv2.Canny(grayImg, threshold1=195, threshold2=250)
        #edges2 = cv2.Canny(grayImg, threshold1=100, threshold2=250)
        #edges3 = cv2.Canny(grayImg, threshold1=195, threshold2=200)
        #edges3 = cv2.Canny(grayImg, threshold1=0, threshold2=255)
        #edges2 = cv2.Canny(grayImg, threshold1=200, threshold2=255)

        edges3 = cv2.Canny(grayImg, threshold1=150, threshold2=255) # Wurde ausgewählt auch andere sicher möglich u. eventuell sinnvoll

        if showChart:
            fig, axes = plt.subplots(nrows=1, ncols=3)
            axes[0].imshow(imageRGB)
            axes[0].set_title('Orginal')

            axes[1].imshow(grayImg, cmap="gray")
            axes[1].set_title('Graubild')

            axes[2].imshow(edges3,"gray")
            axes[2].set_title('Detektierte Kanten')
            plt.show()

        edgeCount = np.mean(edges3)
        edgeCounts = np.append(edgeCounts, edgeCount)

    avgEdgeCount= np.mean(edgeCounts)
    stdEdgeCount= np.std(edgeCounts)

    return [avgEdgeCount, stdEdgeCount]


def calculateGreyCoMatrixMetrics(images):
    """
    Create Graycomatrix and return metrics of it

    Args:
    image (List of NumPy Array): List of values representing an image
    """
    contrasts = np.empty((0,))
    dissimilarities = np.empty((0,))
    homogeneities = np.empty((0,))
    energies = np.empty((0,))
    correlations = np.empty((0,))

    for imageInd in range(0, len(images)):
        image = images[imageInd]
        grayImg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        distances = [1]  # distance between pixels
        angles = [0, np.pi/4, np.pi/2, 3*np.pi/4]  # different angles to create matrix
       
        greycomatrix = graycomatrix(grayImg, distances, angles, symmetric=True, normed=True)

        contrast = graycoprops(greycomatrix, 'contrast')
        dissimilarity = graycoprops(greycomatrix, 'dissimilarity')
        homogeneity = graycoprops(greycomatrix, 'homogeneity')
        energy = graycoprops(greycomatrix, 'energy')
        correlation = graycoprops(greycomatrix, 'correlation')

        contrasts = np.append(contrasts, [contrast])
        dissimilarities = np.append(dissimilarities, [dissimilarity])
        homogeneities = np.append(homogeneities, [homogeneity])
        energies = np.append(energies, [energy])
        correlations = np.append(correlations, [correlation])

    avgGrayContrast = np.mean(contrasts)
    stdGrayContrast = np.std(contrasts)

    avgDissimilarity = np.mean(dissimilarities)
    stdDissimilarity = np.std(dissimilarities)

    avgHomogeneity = np.mean(homogeneities)
    stdHomogeneity = np.std(homogeneities)

    avgEnergy = np.mean(energies)
    stdEnergy = np.std(energies)

    avgCorrelation = np.mean(correlations)
    stdCorrelation = np.std(correlations)

    return [avgGrayContrast, stdGrayContrast, avgDissimilarity, stdDissimilarity, avgHomogeneity, stdHomogeneity, avgEnergy, stdEnergy, avgCorrelation, stdCorrelation]


def avgHistogram(images, colorMode):
    """
    Calculate values to show average histogram for color

    Args:
    image (List of NumPy Array): List of values representing an image
    colorMode (ColorMode): for which color should histogram be calculated

    Returns:
    colList (Array of numbers): found count of color values in image
    bins (Array of numbers): found color values
    """
    colList = np.zeros((256,))
    bins = None
    for imageInd in range(0, len(images)):
        image = images[imageInd]

        if colorMode == ColorMode.all:
            grayImg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            val = grayImg.flatten()
        elif colorMode == ColorMode.red:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            red= np.zeros((224,224), dtype="uint8")
            red[ :, :] = image_rgb[ :, :, 0]
            val = red.flatten()
        elif colorMode == ColorMode.green:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            green= np.zeros((224,224), dtype="uint8")
            green[ :, :] = image_rgb[ :, :, 1]
            val = green.flatten()
        elif colorMode == ColorMode.blue:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            blue= np.zeros((224,224), dtype="uint8")
            blue[ :, :] = image_rgb[ :, :, 2]
            val = blue.flatten()

        counts, bins = np.histogram(val, range(257))
        colList = np.add(colList, counts)
   
    sumList = np.sum(colList)
    colList = np.divide(colList, sumList)
    return colList, bins

def allcolorHistogram(images):
    """
    Calculate values for histogram for all images

    Args:
    image (List of NumPy Array): List of values representing an image

    Returns:
    colList (Array of Array of numbers): found count of color values in image for image and each channel
    bins (Array of Array of numbers): found color values for image and each channel
    """
    colLists = []
    binsList = []

    col, bin = avgHistogram(images, ColorMode.all)
    colLists.append(col)
    binsList.append(bin)

    col, bin = avgHistogram(images, ColorMode.red)
    colLists.append(col)
    binsList.append(bin)

    col, bin = avgHistogram(images, ColorMode.green)
    colLists.append(col)
    binsList.append(bin)

    col, bin = avgHistogram(images, ColorMode.blue)
    colLists.append(col)
    binsList.append(bin)

    return colLists, binsList


def exportToExcel(columNames, data, fileName):
    """
    export table to excel file

    Args:
    column (Array of string): Names of the colums
    data (Array of Array of string): data that should be written in file
    fileName (sting): Name file should have
    """
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(columNames)

    for row in data:
        sheet.append(row)

    workbook.save(fileName)
