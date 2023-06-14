# Was könnte man analysieren?
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os

from config import EPOCHS, PROJECT_ROOT
from excel_export import exportToExcel

def getAverage(image):
    absAvg = np.mean(image)
    channelAvg = np.mean(image, axis=(0, 1)) # Average for each chanel
    return absAvg, channelAvg

def getStd(image):
    allStd = np.std(image)
    channelStd = np.std(image, axis=(0, 1))
    return allStd, channelStd

def printHistogram(vals):
    #vals = image.mean(axis=2).flatten()
    #counts, bins = np.histogram(vals, range(257))
    #print(image.shape)
    #grayImg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #vals = grayImg.flatten()
    counts, bins = np.histogram(vals, range(257), density=True)
   
    plt.bar(bins[:-1] - 0.5, counts, width=1, edgecolor='none')
    plt.xlim([-0.5, 255.5])
    plt.show()

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

def showRGB():
    """
    Show images splitted into each color
    """
    for imageInd in range(0, len(images)):
        image = images[imageInd]
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        fig, ax = plt.subplots(nrows = 1, ncols=4, figsize=(15,5))  

        red= np.zeros(image_rgb.shape, dtype="uint8")
        green= np.zeros(image_rgb.shape, dtype="uint8")
        blue= np.zeros(image_rgb.shape, dtype="uint8") 

        red[ :, :, 0] = image_rgb[ :, :, 0]
        green[ :, :, 1] = image_rgb[ :, :, 1]
        blue[ :, :, 2] = image_rgb[ :, :, 2]

        ax[0].imshow(image_rgb)
        ax[1].imshow(red)
        ax[2].imshow(green)
        ax[3].imshow(blue)
        plt.show()

def plotManyImages(images):
    """
    Plot images to view colors
    """
    
    num_images = 40
    num_rows = 4
    num_cols = 10
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(10, 12))

    # Plot the images
    for i, ax in enumerate(axes.flat):
        if i < num_images:
            image_rgb = cv2.cvtColor(images[i], cv2.COLOR_BGR2RGB)
            ax.imshow(image_rgb)  # Use 'gray' colormap for grayscale images
            ax.axis('off')
        else:
            ax.axis('off') 
    
    plt.tight_layout()
    plt.show()


def extractEdges(images, showChart = False):
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

def avgHistogram(images):
    colList = np.empty((0,))
    for imageInd in range(0, len(images)):
        image = images[imageInd]
        grayImg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        val = grayImg.flatten()
        colList = np.append(colList, val)

    print(colList.shape)
    printHistogram(colList)

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

#avgHistogram(images) # Idee: Werte direkt addieren => pro Bin ein Wert nur gespeichert => hoffentlicher schneller

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