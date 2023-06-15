import numpy as np
import matplotlib.pyplot as plt
import cv2

def showRGB(images):
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

def viewHistogram(colList, bins):
    plt.bar(bins[:-1] -0.5, colList, width=1, edgecolor='none')
    plt.xlim([-0.5, 255.5])
    plt.show()


def viewColorsHistogram(colsList, binList):
    fig, axes = plt.subplots(1, 4)
    axes[0].bar(binList[0][:-1] -0.5, colsList[0], width=1, edgecolor='none')
    axes[0].set_title('All Colors')

    axes[1].bar(binList[1][:-1] -0.5, colsList[1], width=1, edgecolor='none')
    axes[1].set_title('Red')

    axes[2].bar(binList[2][:-1] -0.5, colsList[2], width=1, edgecolor='none')
    axes[2].set_title('Green')

    axes[3].bar(binList[3][:-1] -0.5, colsList[3], width=1, edgecolor='none')
    axes[3].set_title('Blue')

    fig.tight_layout(pad=0.2)
    plt.show()




