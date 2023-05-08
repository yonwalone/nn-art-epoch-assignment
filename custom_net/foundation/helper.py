def print_progress_bar(amount, of, start_text = "Progress", end_text = "", new_line = True):
    amount += 1
    progress = int(((amount)/of)*100)
    progress_bar = f"{start_text}: [{'='*int(progress/2)}{' '*(50-int(progress/2))}] {progress}% ({amount}/{of}) {end_text}"
    print(progress_bar, end="\r" if not new_line and progress < 100 else "\n")

def flatInput(array):
    """
    Convert arrray with multible dimensions including numbers, to array of numbers
    Params:
        -  array: array with multible dimensions
    
    Returns:
        - output: array with one dimension
    """
    output= []
    for a in array:
        if isinstance(a, float) or isinstance(a, int):
            output.append(a)
        else:
            output += flatInput(a)
    return output


def preprocessImages(images):
    """
    Preprocess images for each image in list

    Params:
        - images: list of images
    
    Returns:
        - newImages: list of transformed images
    """
    newImages = []
    for imageIndex in range(0, len(images)):
        newImages.append(preprocessImage(images[imageIndex]))
    return newImages


def preprocessImage(image):
    """
    Convert image to expected formage

    Params:
        - image: input image [height [width [inputDepth]]] or [height [width]]

    Returns:
        - newImage: transformed image[inputDepth [height [width]]]
    """
    newImage = []
    if isinstance(image[0][0], float) or isinstance(image[0][0], int):
        # case 2
        newImage = [image]
    else:
        # case 1
        newImage = [[[0 for _ in range(0, len(image[0]))] for _ in range(0, len(image))] for _ in range(0, len(image[0][0]))]
        for row in range(0, len(image)):
            for col in range(0, len(image[0])):
                for inDepth in range(0, len(image[0][0])):
                    newImage[inDepth][row][col] = image[row][col][inDepth]

    return newImage


def printStatistics(results, label):
    """
    Params:
        - results: [expected result, result]
    """
    for resIndex in range(0, len(results)):

        sum = 0
        for i in range(0, len(results[resIndex])):
            sum += results[resIndex][i]

        print(f"For Label {label[resIndex]} following results: {results[resIndex][resIndex] / sum}")

        for i in range(0, len(results[resIndex])):
            print(f"{label[i]}: {results[resIndex][i]/sum}")
        
        print("---------------------------------------")

    chosenClasses = [ 0 for _ in range(0, len(results))]
    allresults = 0

    for resIndex in range(0, len(results)):
        
        for i in range(0, len(results[resIndex])):
            chosenClasses[i] += results[resIndex][i]
            allresults += results[resIndex][i]
    
    print("Recieved Lables:")
    for i in range(0, len(results)):
        print(f"{label[i]}: {chosenClasses[i] / allresults}")

