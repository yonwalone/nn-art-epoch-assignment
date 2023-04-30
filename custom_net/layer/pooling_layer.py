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
        self.image = image[:]

        # Find (max/avg) number in each frame
        necessaryRows = int((len(image) - self.poolSize)/self.stride + 1)
        necessaryColumns = int((len(image[0]) - self.poolSize)/self.stride + 1)

        newImage=[]
        for rowIndex in range(0, necessaryRows):
            newRow = []
            for columnIndex in range(0, necessaryColumns):
                # Get value for field
                results = []
                for poolRowIndex in range(0, self.poolSize):
                    for poolColIndex in range(0, self.poolSize):
                        results.append(image[rowIndex * self.stride + poolRowIndex][columnIndex * self.stride + poolColIndex])
                
                if self.function == Functions.max:
                    newRow.append(max(results))
                elif self.function == Functions.avg:
                    newRow.append(int(sum(results) / len(results)))
                else:
                    raise Exception("Use valid pooling function")

                
            newImage.append(newRow)

        #print(newImage)

        return newImage
    
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

        # Get index of maximum value per frame
        relevantIndexes = []
        necessaryRows = int((len(self.image) - self.poolSize)/self.stride + 1)
        necessaryColumns = int((len(self.image[0]) - self.poolSize)/self.stride + 1)

        for rowIndex in range(0, necessaryRows):
            for columnIndex in range(0, necessaryColumns):

                # Get values in frame
                results = []
                for poolRowIndex in range(0, self.poolSize):
                    for poolColIndex in range(0, self.poolSize):
                        results.append(self.image[rowIndex * self.stride + poolRowIndex][columnIndex * self.stride + poolColIndex])
                
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

                relevantIndexes.append([yPosAbsolute, xPosAbsolute])

        # generate image filled with 0
        resultImage = [[0 for _ in self.image[0]] for _ in self.image]
                

        # derivates on position where number taken for pooling 
        for derivateIndex, derivate in enumerate(targets):
            resultImage[relevantIndexes[derivateIndex][0]][relevantIndexes[derivateIndex][1]] = derivate

        #print(f"Hanle Error Result Pooling: {resultImage}")

        return resultImage
    
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
