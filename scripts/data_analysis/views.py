import numpy as np
import matplotlib.pyplot as plt
import cv2
from config import EPOCHS

def showRGB(images):
    """
    Show images splitted into each color
    
    Args:
    images (list): List including images
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

    Args:
    images (list): List including images
    """
    num_images = 40
    num_rows = 4
    num_cols = 10
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(10, 12))

    # Plot the images
    for i, ax in enumerate(axes.flat):
        if i < num_images:
            image_rgb = cv2.cvtColor(images[i], cv2.COLOR_BGR2RGB)
            ax.imshow(image_rgb)
            ax.axis('off')
        else:
            ax.axis('off') 
    
    plt.tight_layout()
    plt.show()


def viewHistogram(colList, bins):
    """
    Show single histogram

    Args:
    colList (list): List of numbers representing values to show
    bins (list): List of numbers representing indexes indicating the places to show columns
    """
    plt.bar(bins[:-1] -0.5, colList, width=1, edgecolor='none')
    plt.xlim([-0.5, 255.5])
    plt.show()


def viewColorsHistogram(colsList, binList, epoch):
    """
    View histograms for complet image and each channel

    Args:
    colList (2dim list): List of numbers representing values to show
    binList (2dim list): List of numbers representing indexes indicating the places to show columns
    epoch string: Name of epoch
    """
    fig, axes = plt.subplots(1, 4, figsize=(12, 3), sharey= True)
    fig.suptitle(epoch, fontsize=16, y=0.95)

    axes[0].bar(binList[0][:-1] -0.5, colsList[0], width=1, edgecolor='none')
    axes[0].set_title('All Colors')

    axes[1].bar(binList[1][:-1] -0.5, colsList[1], width=1, edgecolor='none')
    axes[1].set_title('Red')

    axes[2].bar(binList[2][:-1] -0.5, colsList[2], width=1, edgecolor='none')
    axes[2].set_title('Green')

    axes[3].bar(binList[3][:-1] -0.5, colsList[3], width=1, edgecolor='none')
    axes[3].set_title('Blue')

    fig.tight_layout(pad=1)
    plt.subplots_adjust(wspace=0.4)
    plt.show()


def viewAllHistogram(colList, binList):
    """
    View histograms of all epochs and for each with complete image and each channel

    Args:
    colList (3dim list): List of numbers representing values to show
    binList (3dim list): List of numbers representing indexes indicating the places to show columns
    """
    histPerRow = 4
    countRows = 10
    countHistograms = histPerRow * countRows

    fig, axs = plt.subplots(countRows, histPerRow, figsize=(15, 30), sharey= True)
    axs = axs.flatten()

    # Plot each histogram
    for row in range(countRows):
        for col in range(histPerRow):
            axs[4*row+col].bar(binList[row][col][:-1] -0.5, colList[row][col], width=1, edgecolor='none')
            axs[4*row+col].set_ylim(0.0, 0.015)
            if row == 0:
                if col == 0:
                    axs[4*row+col].set_title("All Colors")
                elif col == 1:
                    axs[4*row+col].set_title("Red")
                elif col == 2:
                    axs[4*row+col].set_title("Green")
                elif col == 3:
                    axs[4*row+col].set_title("Blue")

    # Add labels
    for col in range(countRows):
        axs[col * histPerRow].text(-0.3, 0.5, EPOCHS[col], transform=axs[col * histPerRow].transAxes,
                                rotation=90, ha='center', va='center')

    # Remove empty subplots
    if countHistograms < len(axs):
        for col in range(countHistograms, len(axs)):
            fig.delaxes(axs[col])
    
    fig.tight_layout(pad=1.5)
    plt.subplots_adjust(wspace=0.4)
    plt.show()
