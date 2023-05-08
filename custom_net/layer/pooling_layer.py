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
                        newRow.append(sum(results) / len(results))
                    else:
                        raise Exception("Use valid pooling function")
                    
                newImage.append(newRow)

            outImages.append(newImage)

        #print(f"Pooling Out: {outImages}")
        return outImages
    

    def handleError(self, targets, errorFunc, learningRate):
        """
        Handle error for layer, change weights of matrix and propagate error further

        Params:
            -  targets: recieved error
            -  errorFunc: error function to initially calculate error
            -  learningRate (Float): Factor how strong weights are changed based on error

        Return:
            - errors: propagage errors further

        """

        resultImages=[]
        target = 0

        # Get index of for error relevant elements per frame
        for depth in range(0, len(self.images)):

            # generate image filled with 0
            resultImage = [[0 for _ in self.images[depth][0]] for _ in self.images[depth]]   

            necessaryRows = int((len(self.images[depth]) - self.poolSize)/self.stride + 1)
            necessaryColumns = int((len(self.images[depth][0]) - self.poolSize)/self.stride + 1)

            for rowIndex in range(0, necessaryRows):
                for columnIndex in range(0, necessaryColumns):

                    # Get values in frame
                    results = []
                    for poolRowIndex in range(0, self.poolSize):
                        for poolColIndex in range(0, self.poolSize):
                            results.append(self.images[depth][rowIndex * self.stride + poolRowIndex][columnIndex * self.stride + poolColIndex])
                               
                    if self.function == Functions.max:
                        relevantPos = 0
                        result = max(results)
                        relevantPos = results.index(result)

                        #Positions of number in frame
                        yPosPattern = int(relevantPos/self.poolSize)
                        xPosPattern = relevantPos % self.poolSize

                        # Position of number in image
                        yPosAbsolute = rowIndex * self.stride + yPosPattern
                        xPosAbsolute = columnIndex * self.stride + xPosPattern

                        resultImage[yPosAbsolute][xPosAbsolute] = targets[target]

                    elif self.function == Functions.avg:
                        for poolRowIndex in range(0, self.poolSize):
                            for poolColIndex in range(0, self.poolSize):
                                resultImage[rowIndex * self.stride + poolRowIndex][columnIndex * self.stride + poolColIndex] += targets[target] / self.poolSize /self.poolSize #* len(results) / self.images[depth][rowIndex * self.stride + poolRowIndex][columnIndex * self.stride + poolColIndex]

                    else:
                        raise Exception("Use valid pooling function")

                    target += 1
              
            resultImages.append(resultImage)
        return resultImages
    
    
    def getStructure(self):
        """
        Get structure of layer

        Returns:
        - 
        """
        return [LayerType.pool.value, [self.function.value, self.poolSize, self.stride]]
