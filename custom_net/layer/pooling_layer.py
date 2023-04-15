from foundation.functions import Functions
from layer.layer_interface import LayerInterface

class PoolLayer(LayerInterface):

    def __init__(self, function= Functions.max, poolSize = 2, stride=1, toList = False):
        """
        Initialize convolutional layer.

        Args:
            - fuction (Functions): Pooling Function to be used in process
            - poolSize (Int): Width and length of area which should be used for pooling
            - stride (Int): Distance to move over image between pooling
            - toList (Bool): Should information be converted into an Array
        """
        self.poolSize = poolSize
        self.stride = stride
        self.function = function
        self.toList = toList

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
        for row in range(0, necessaryRows):
            newRow = []
            for column in range(0, necessaryColumns):
                # Get value for field
                results = []
                for poolRow in range(0, self.poolSize):
                    for poolCol in range(0, self.poolSize):
                        results.append(image[row * self.stride + poolRow][column * self.stride + poolCol])
                
                result = None
                if self.function == Functions.max:
                    result = max(results)

                if self.function == Functions.avg:
                    result = int(sum(results) / len(results))

                if result == None:
                    raise Exception("Use valid pooling function")

                newRow.append(result)
            newImage.append(newRow)

        # Convert to 1dim list
        if self.toList:
            newList = []
            for index in range(0, len(newImage)):
                newList += newImage[index]

            # Append 1 as bias for next layer
            newList.append(1)
            newImage = newList

        return newImage
    
    def handleError(self, targets, errorFunc, learningRate): # currently only implemeted for max function
        """
        Handle error for layer, change weights of matrix and propagate error further

        Params:
            -  targets: recieved error / expected output at last layer
            -  errorFunc: error function to initially calculate error
            -  learningRate (Float): Factor how strong weights are changed based on error

        Return:
            - errors: propagage errors further

        """

        # Get index of maximum value per frame
        maxIndexes = []
        necessaryRows = int((len(self.image) - self.poolSize)/self.stride + 1)
        necessaryColumns = int((len(self.image[0]) - self.poolSize)/self.stride + 1)

        for row in range(0, necessaryRows):
            for column in range(0, necessaryColumns):

                # Get values in frame
                results = []
                for poolRow in range(0, self.poolSize):
                    for poolCol in range(0, self.poolSize):
                        results.append(self.image[row * self.stride + poolRow][column * self.stride + poolCol])
                
                result = max(results)

                posInArray = results.index(result)

                #Positions of number in frame
                yPosPattern = int(posInArray/self.poolSize)
                xPosPattern = posInArray % self.poolSize

                # Position of number in image
                yPosAbsolute = row * self.stride + yPosPattern
                xPosAbsolute = column * self.stride + xPosPattern

                maxIndexes.append([yPosAbsolute, xPosAbsolute])

        # generate image filled with 0
        resultImage = []
        for row in range(0,len(self.image)):
            imageRow = []
            for col in range(0,len(self.image[0])):
                imageRow.append(0)
            resultImage.append(imageRow)

        # add incoming derivate together
        derivateIn = []
        for index in range(0,len(targets)):
            value = 0
            for val in range(0, len(targets[index])):
                value += targets[int(index)][int(val)]
                #print(value)
            derivateIn.append(value)

        # derivates on position where number taken for pooling 
        for derivateIndex in range(0, len(derivateIn)):
            resultImage[maxIndexes[derivateIndex][0]][maxIndexes[derivateIndex][1]] = derivateIn[derivateIndex]

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
        return None
