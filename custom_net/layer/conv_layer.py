from foundation.enums import PaddingType, LayerType
from layer.layer_interface import LayerInterface

class CONVLayer(LayerInterface):

    def __init__(self, matrix, stride = 1, padding = PaddingType.valid):
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

        # Check if matrix is allowed
        if any(len(row) != len(self.matrix[0]) for row in self.matrix):
            raise Exception("Matrix must have the same width in all rows")

            
    def act(self, image):
        """
        Transform image based on the settings of the layer.

        Args:
            - image (2dim Array): Image to put into layer

        Return:
            - newImage: Transformed image 
        """

        #print(f"Act Input: {image}")

        # Add padding around image
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

        #print(f"Conv Output: {newImage}")

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
        paddingNumber = 0
        matLen = len(self.matrix)
        if self.padding == PaddingType.same:
            paddingNumber = max(matLen - self.stride, 0) // 2 
        if self.padding == PaddingType.full:
            paddingNumber = matLen - 1

        newImage = []
        
        # Padding lines
        paddingLine = [0] * (len(image[0]) + 2 * paddingNumber)

        # Append start padding
        newImage.extend([paddingLine] * paddingNumber)

        # Add padding to beginning and end of each row
        for row in image:
            padded_row = [0] * paddingNumber + row + [0] * paddingNumber
            newImage.append(padded_row)

        # Append end padding
        newImage.extend([paddingLine] * paddingNumber)

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

        outputLen = len(self.image) - len(self.matrix) - self.stride  + 2


        #print(f"Input: {targets}")
        #print(f"Image: {self.image}")

        # Calculate kernal gradients
        kernalGradient = [[0 for _ in self.matrix[0]] for _ in self.matrix]

        #print(f"Lange Targets: {len(targets)}")
        #print(f"Lange Image: {len(self.image)}")

        necessaryRows = int((len(self.image) - len(targets))/self.stride + 1)
        necessaryColumns = int((len(self.image[0]) - len(targets[0]))/self.stride + 1)

        #print(necessaryRows)
        #print(necessaryColumns)

        # Move targets over image
        for rowIndex in range(0, necessaryRows):
            for columnIndex in range(0, necessaryColumns):

                val = 0
                for targetRowIndex in range(0, len(targets)):
                    for targetColIndex in range(0, len(targets[0])):
                        val += self.image[rowIndex * self.stride + targetRowIndex][columnIndex * self.stride + targetColIndex] * targets[targetRowIndex][targetColIndex]
                kernalGradient[rowIndex][columnIndex] = val

        #print(f"KernalGradient: {kernalGradient}")

        # Calculate input gradients

        # pad output gradient with 0 around
        extendedGradient = []

        firstline = []
        for i in range(0, len(targets[0]) + 2):
            firstline.append(0) 
        extendedGradient.append(firstline)

        for i in range(0, len(targets)):
            line = [0]
            line += targets[i]
            line += [0]
            extendedGradient.append(line)

        extendedGradient.append(firstline)

        #print(extendedGradient)

        necessaryRows = int((len(extendedGradient) - len(self.matrix))/self.stride + 1)
        necessaryColumns = int((len(extendedGradient[0]) - len(self.matrix[0]))/self.stride + 1)

        inputGradients = [[0 for _ in range(0, necessaryColumns)] for _ in range(0, necessaryRows)]

        # Move matrix over extended gradients
        for rowIndex in range(0, necessaryRows):
            for columnIndex in range(0, necessaryColumns):

                val = 0
                for targetRowIndex in range(0, len(self.matrix)):
                    for targetColIndex in range(0, len(self.matrix[0])):
                        val += extendedGradient[rowIndex * self.stride + targetRowIndex][columnIndex * self.stride + targetColIndex] * self.matrix[targetRowIndex][targetColIndex]
                inputGradients[rowIndex][columnIndex] = val


        # Adapt Gradients of matrix
        for rowIndex in range(0, len(self.matrix)):
            for rowCol in range(0, len(self.matrix[0])):
                self.matrix[rowIndex][rowCol] -= learningRate * kernalGradient[rowIndex][rowCol]
        #print(self.matrix)

        # convert outputs to 1dim list
        errors = []
        for rowIndex in range(0, len(inputGradients)):
            for colIndex in range(0, len(inputGradients[rowIndex])):
                errors.append(inputGradients[rowIndex][colIndex])

        return errors

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
        return [LayerType.conv.value, [self.getWeights(), self.stride, self.padding.value]]
 