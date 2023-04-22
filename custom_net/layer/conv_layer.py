from layer.layer_interface import LayerInterface

class CONVLayer(LayerInterface):

    def __init__(self, matrix, stride = 1, padding = False):
        """
        Initialize convolutional layer.

        Args:
            - matrix (2dim Array): Matrix to use in transformation
            - stride (Int): Distance to move matrix over image
            - padding (Bool): Should padding be added to image
        """
        self.matrix = matrix
        self.stride = stride
        self.padding = padding

        # Check if matrix is square
        for parameterIndex in range(0, len(self.matrix)):
            if(len(self.matrix[parameterIndex]) != len(self.matrix[0])):
                raise Exception("Matrix must has the same width in all rows")
            
    def act(self, image):
        """
        Transform image based on the settings of the layer.

        Args:
            - image (2dim Array): Image to put into layer

        Return:
            - newImage: Transformed image 
        """

        # Add padding around image
        if self.padding:
            image = self.addPadding(image)
            
        self.image = image 

        # evaluate how often the matrix is moved down and moved right per row
        necessaryRows = int((len(image) - len(self.matrix))/self.stride + 1)
        necessaryColumns = int((len(image[0]) - len(self.matrix[0]))/self.stride + 1)
        
        # move matrix over image
        newImage = []
        for row in range(0, necessaryRows):
            newRow = []
            for column in range(0, necessaryColumns):
                # multiply elements at the same spot in frame and add it together
                result = 0
                for matrixRow in range(0, len(self.matrix)):
                    for matrixCol in range(0, len(self.matrix[0])):
                        result += self.matrix[matrixRow][matrixCol] * image[row * self.stride + matrixRow][column * self.stride + matrixCol]

                newRow.append(result)
            newImage.append(newRow)

        return newImage

    def addPadding(self, image):
        """
        Add padding with number 0 around the image with the width based on the matrix size

        Params:
            - image (2dim Array): Image to be padded

        Return:
            - newImage (2dim Array): Image with padding

        """
        #TODO: Support smaller padding
        paddingNumber = len(self.matrix) -1 # Expect square

        paddingNumber = 1

        newImage = []
        
        # Padding lines
        paddingLine = []
        for i in range(0, len(image[0]) + 2 * paddingNumber):
            paddingLine.append(0)

        #Append start padding
        for index in range(0, paddingNumber):
            newImage.append(paddingLine)
           
        #Add padding to begin and ending of line
        for line in range(0, len(image)):
            imageLine = []
            for index in range(0, paddingNumber):
                imageLine.append(0)
            imageLine += image[line]
            for index in range(0, paddingNumber):
                imageLine.append(0)
            newImage.append(imageLine)

        #Append end padding
        for index in range(0, paddingNumber):
            newImage.append(paddingLine)

        return newImage


    def handleError(self, targets, errorFunc, learningRate):
        """
        Handle error for layer, change weights of matrix and propagate error further

        Params:
            -  targets: recieved error / expected output at last layer
            -  errorFunc: error function to initially calculate error
            -  learningRate (Float): Factor how strong weights are changed based on error

        Return:
            - errors: propagage errors further

        """
        #print("Handle")
        # evaluate how often the matrix is moved down and moved right per row
        necessaryRows = int((len(self.image) - len(self.matrix))/self.stride + 1)
        necessaryColumns = int((len(self.image[0]) - len(self.matrix[0]))/self.stride + 1)

        if (necessaryRows * necessaryColumns != len(targets) * len(targets[0])):
            raise Exception("Number of targets must match number of patches")
        
        #print(self.matrix)

        for row in range(0, necessaryRows):
            newRow = []
            for column in range(0, necessaryColumns):
                if targets[row][column] == 0:
                    continue

                # For all patches  
                for matrixRow in range(0, len(self.matrix)):
                    for matrixCol in range(0, len(self.matrix[0])):
                        self.matrix[matrixRow][matrixCol] += learningRate * self.matrix[matrixRow][matrixCol] * targets[row][column] * self.image[row * self.stride + matrixRow][column * self.stride + matrixCol]
                
        #print(self.matrix)

        return None

    def getWeights(self):
        """
        Get weights of layer

        Returns:
        - 
        """
        return self.matrix
    

    def getStructure(self):
        """
        Get structure of layer

        Returns:
        - 
        """
        pass
 