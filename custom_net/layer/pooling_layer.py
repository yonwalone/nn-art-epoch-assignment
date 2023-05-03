from foundation.enums import Functions, LayerType
from layer.layer_interface import LayerInterface

class PoolLayer(LayerInterface):

    def __init__(self, function= Functions.max, poolSize = 2, stride=1):
        """
        Initialize convolutional layer.

        Args:
            - fuction (Functions): Pooling Function to be used in process
            - poolSize (Int): Width and length of area which should be used for pooling
            - stride (Int): Distance to move over image between pooling
        """
        self.function = function
        self.poolSize = poolSize
        self.stride = stride

    def act(self, image):
        """
        Transform image based on the settings of the layer.

        Args:
            - image (2dim Array): Image to put into layer

        Return:
            - newImage: Transformed image 
        """
        self.images = image[:]

        outImages = []
        for img in self.images:
            #print(f"Pool Image height: {len(img)}")
            #print(f"Pool Image width: {len(img[0])}")
            # Find (max/avg) number in each frame
            necessaryRows = int((len(img) - self.poolSize)/self.stride + 1)
            necessaryColumns = int((len(img[0]) - self.poolSize)/self.stride + 1)

            newImage=[]
            for rowIndex in range(0, necessaryRows):
                newRow = []
                for columnIndex in range(0, necessaryColumns):
                    # Get value for field
                    results = []
                    for poolRowIndex in range(0, self.poolSize):
                        for poolColIndex in range(0, self.poolSize):
                            results.append(img[rowIndex * self.stride + poolRowIndex][columnIndex * self.stride + poolColIndex])
                    
                    if self.function == Functions.max:
                        newRow.append(max(results))
                    elif self.function == Functions.avg:
                        newRow.append(int(sum(results) / len(results)))
                    else:
                        raise Exception("Use valid pooling function")
                    
                newImage.append(newRow)

            outImages.append(newImage)

        #print(f"Pooling Out: {outImages}")
        return outImages
    
    def handleError(self, targets, errorFunc, learningRate): # currently only implemeted for max function
        """
        Handle error for layer, change weights of matrix and propagate error further

        Params:
            -  targets: recieved error
            -  errorFunc: error function to initially calculate error
            -  learningRate (Float): Factor how strong weights are changed based on error

        Return:
            - errors: propagage errors further

        """
        #print(f"Targets: {targets}")

        resultImages=[]
        target = 0

        # Get index of for error relevant elements per frame
        for depth in range(0, len(self.images)):
            #relevantIndexes = []
            #print("Start depth")

            # generate image filled with 0
            resultImage = [[0 for _ in self.images[depth][0]] for _ in self.images[depth]]   

            necessaryRows = int((len(self.images[depth]) - self.poolSize)/self.stride + 1)
            necessaryColumns = int((len(self.images[depth][0]) - self.poolSize)/self.stride + 1)

            #print(necessaryRows)
            #print(necessaryColumns)

            for rowIndex in range(0, necessaryRows):
                for columnIndex in range(0, necessaryColumns):

                    # Get values in frame
                    results = []
                    for poolRowIndex in range(0, self.poolSize):
                        for poolColIndex in range(0, self.poolSize):
                            results.append(self.images[depth][rowIndex * self.stride + poolRowIndex][columnIndex * self.stride + poolColIndex])
                    
                    relevantPos = 0
                    if self.function == Functions.max:
                        result = max(results)
                        relevantPos = results.index(result)
                    else:
                        raise Exception("Use valid pooling function")

                    #Positions of number in frame
                    yPosPattern = int(relevantPos/self.poolSize)
                    xPosPattern = relevantPos % self.poolSize

                    # Position of number in image
                    yPosAbsolute = rowIndex * self.stride + yPosPattern
                    xPosAbsolute = columnIndex * self.stride + xPosPattern

                    #relevantIndexes.append([yPosAbsolute, xPosAbsolute])
                    resultImage[yPosAbsolute][xPosAbsolute] = targets[target]
                    target += 1
              
            # derivates on position where number taken for pooling 
            #for derivateIndex in range(0, len(targets) - priorIndexes):
            #    if derivateIndex < len(relevantIndexes):
            #        resultImage[relevantIndexes[derivateIndex][0]][relevantIndexes[derivateIndex][1]] = targets[priorIndexes+derivateIndex]
            #    else:
            #        priorIndexes += derivateIndex
            #        break

            #print(f"Hanle Error Result Pooling: {resultImage}")
            #print(f"Height Img: {len(resultImage)}")
            #print(f"Height Img: {len(resultImage[0])}")
            resultImages.append(resultImage)
        #print(len(resultImages))
        #print(len(resultImage[0]))
        #print(target)
        #print(resultImages)
        return resultImages
    
    def getWeights(self):
        """
        Get weights of layer

        Returns:
        - 
        """
        return None
    
    def getStructure(self):
        """
        Get structure of layer

        Returns:
        - 
        """
        return [LayerType.pool.value, [self.function.value, self.poolSize, self.stride]]
