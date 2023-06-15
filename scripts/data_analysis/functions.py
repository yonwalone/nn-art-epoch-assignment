import numpy as np
import matplotlib.pyplot as plt
import cv2
from excel_export import ColorMode

def getAverage(image):
    absAvg = np.mean(image)
    channelAvg = np.mean(image, axis=(0, 1)) # Average for each chanel
    return absAvg, channelAvg

def getStd(image):
    allStd = np.std(image)
    channelStd = np.std(image, axis=(0, 1))
    return allStd, channelStd

def calculateColorAverages(images):
    """
    Calculate information about the use of color in the images
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
    """
    edgeCounts = np.empty((0,))
    for imageInd in range(0, len(images)):
        image = images[imageInd]
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        grayImg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #edges = cv2.Canny(grayImg, threshold1=195, threshold2=250)
        #edges2 = cv2.Canny(grayImg, threshold1=100, threshold2=250)
        #edges3 = cv2.Canny(grayImg, threshold1=195, threshold2=200)
        #edges3 = cv2.Canny(grayImg, threshold1=0, threshold2=255)
        #edges2 = cv2.Canny(grayImg, threshold1=200, threshold2=255)

        edges3 = cv2.Canny(grayImg, threshold1=150, threshold2=255) # Wurde ausgewählt auch andere sicher möglich u. eventuell sinnvoll

        if showChart:
            fig, axes = plt.subplots(nrows=1, ncols=3)
            axes[0].imshow(image_rgb)
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


def avgHistogram(images, colorMode):
    """
    Calculate values to show average histogram for color
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



