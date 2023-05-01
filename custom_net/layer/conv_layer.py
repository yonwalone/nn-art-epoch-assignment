from foundation.enums import PaddingType, LayerType
from layer.layer_interface import LayerInterface
import random as rnd

class CONVLayer(LayerInterface):

    def __init__(self, matrix = 3, stride = 1, padding = PaddingType.valid):
        """
        Initialize convolutional layer.

        Args:
            - matrix (2dim Array): Matrix to use in transformation
            - stride (Int): Distance to move matrix over image
            - padding (Bool): Should padding be added to image
        """
        if type(matrix) == int:
            self.matrix = []
            for index in range(0, matrix):
                row = []
                for i in range(0, matrix):
                    row.append(rnd.random())
                self.matrix.append(row)
                

        else:
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

        #print(f"Len Input: {len(image)}")

        # Add padding around image
        image = self.addPadding(image)
            
        self.image = image 

        if (len(image) - len(self.matrix))/self.stride % 1 != 0.0 or (len(image[0]) - len(self.matrix[0]))/self.stride % 1  != 0:
            raise Exception(f"Size of matrix, stride and image does not fit together, change matrix or stride")


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
        #print(f"Lenge Outputs: {len(newImage)}")

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

        #print(f"Padding Number: {paddingNumber}")

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

        #print(f"Input: {targets}")
        #print(f"Image: {self.image}")

        ### Calculate  gradients to improve matrix
        kernalGradient = [[0 for _ in self.matrix[0]] for _ in self.matrix]

        #print(f"Lange Targets: {len(targets)}")
        #print(f"Lange Image: {len(self.image)}")

        #Add zeros between targets based on stride
        # [[a,b],
        # [c,d]]
        # To:
        # [[a,0,b],
        # [0,0,0],
        # [c,0,d]]

        extendedGradient = []

        internalPadding = []
        for i in range(0, self.stride -1 ):
            internalPadding.append(0)
        
        for i in range(0, len(targets)):
            row = []
            for j in range(0, len(targets[0])):
                row.append(targets[i][j])
                row += internalPadding

            #print(f"Row:  {row}")
            if self.stride > 1:
                row = row[:-(self.stride-1)]
            #print(f"Mod Row: {row}")
            extendedGradient.append(row)
            
            zeroRow = []
            for j in range(0, len(row)):
                zeroRow.append(0)

            for j in range(0, self.stride -1):
                extendedGradient.append(zeroRow)

        if self.stride > 1:
            extendedGradient = extendedGradient[:-(self.stride-1)]

        necessaryRows = int((len(self.image) - len(extendedGradient)) +1)
        necessaryColumns = int((len(self.image[0]) - len(extendedGradient[0])) +1)

        # Move targets over image
        for rowIndex in range(0, necessaryRows):
            for columnIndex in range(0, necessaryColumns):

                val = 0
                for targetRowIndex in range(0, len(extendedGradient)):
                    for targetColIndex in range(0, len(extendedGradient[0])):
                        val += self.image[rowIndex + targetRowIndex][columnIndex + targetColIndex] * extendedGradient[targetRowIndex][targetColIndex]
                kernalGradient[rowIndex][columnIndex] = val

        # Calculate input gradients

        #print(f"Lange Input Gradients: {len(targets)}")

        ### Calculate errors to propagate further

        # pad extended gradient with zeros around 
        paddedGradient = []

        firstline = []
        for i in range(0, len(extendedGradient[0]) + 2 * (len(self.matrix) - 1)):
            firstline.append(0)
        #print(f"Lange First Line: {len(firstline)}")

        for i in range(0, len(self.matrix) -1):
            paddedGradient.append(firstline)

        for i in range(0, len(extendedGradient)):
            line = []
            for j in range(0, len(self.matrix) -1):
                line.append(0)
            line += extendedGradient[i]
            for j in range(0, len(self.matrix) -1):
                line.append(0)
            paddedGradient.append(line)

        for i in range(0, len(self.matrix) -1):
            paddedGradient.append(firstline)

        #print(f"Lange Extended Gradients: {len(extendedGradient)}")
        #print(f"Lange Padded Gradients: {len(paddedGradient)}")

        # Turn matrix around 180 degree
        turnedMatrix=[]
        for row in reversed(self.matrix):
            newRow = []
            for col in reversed(row):
                newRow.append(col)
            turnedMatrix.append(newRow)

        #print(f"Turned Matrix: {turnedMatrix}")

        necessaryRows = int((len(paddedGradient) - len(turnedMatrix)) + 1)
        necessaryColumns = int((len(paddedGradient[0]) - len(turnedMatrix[0])) + 1)

        #print(necessaryRows)
        #print(necessaryColumns)

        inputGradients = [[0 for _ in range(0, necessaryColumns)] for _ in range(0, necessaryRows)]

        # Move matrix over extended gradients
        for rowIndex in range(0, necessaryRows):
            for columnIndex in range(0, necessaryColumns):

                val = 0
                for targetRowIndex in range(0, len(turnedMatrix)):
                    for targetColIndex in range(0, len(turnedMatrix[0])):
                        val += paddedGradient[rowIndex + targetRowIndex][columnIndex + targetColIndex] * turnedMatrix[targetRowIndex][targetColIndex]
                inputGradients[rowIndex][columnIndex] = val

        ### Adapt Gradients of matrix
        for rowIndex in range(0, len(self.matrix)):
            for rowCol in range(0, len(self.matrix[0])):
                self.matrix[rowIndex][rowCol] -= learningRate * kernalGradient[rowIndex][rowCol]

        #print(len(inputGradients))      ### TODO: Length of input gradients should match input image ( - padding)

        ### Convert image gradients to 1dim array
        errors = []
        for rowIndex in range(0, len(inputGradients)):
            for colIndex in range(0, len(inputGradients[rowIndex])):
                errors.append(inputGradients[rowIndex][colIndex])

        #print(len(errors))

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
 