import random as rnd

from foundation.enums import PaddingType, LayerType
from layer.layer_interface import LayerInterface

class CONVLayer(LayerInterface):
    ### Possibility for more than one matrix, add biases

    def __init__(self, matrix = 3, stride = 1, inputDepth = 3, depth = 1, padding = PaddingType.valid):
        """
        Initialize convolutional layer.

        Args:
            - matrix (2dim Array): Matrix to use in transformation
            - stride (Int): Distance to move matrix over image
            - padding (Bool): Should padding be added to image
        """
        if type(matrix) == int:
            self.matrixes = []
            for d in range(0, depth):
                row = []
                for index in range(0, matrix):
                    spot = []
                    for i in range(0, matrix):
                        place = []
                        for inp in range(0, inputDepth):
                            place.append(rnd.random())
                        spot.append(place)
                    row.append(spot)
                self.matrixes.append(row)       

        else:
            self.matrixes = matrix

        self.stride = stride
        self.padding = padding
        self.inputDepth = inputDepth
        self.depth = depth

        # Check if matrix is allowed
        if any(len(row) != len(self.matrixes[0]) for row in self.matrixes):
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

        if (len(image) - len(self.matrixes[0]))/self.stride % 1 != 0.0 or (len(image[0]) - len(self.matrixes[0][0]))/self.stride % 1  != 0:
            raise Exception(f"Size of matrix, stride and image does not fit together, change matrix or stride")

        # evaluate how often the matrix is moved down and moved right per row
        necessaryRows = int((len(image) - len(self.matrixes[0]))/self.stride + 1)
        necessaryColumns = int((len(image[0]) - len(self.matrixes[0][0]))/self.stride + 1)
        
        # move matrix over image
        newImages = []
        for depth in range(0, self.depth):
            newImage = []
            for row in range(0, necessaryRows):
                newRow = []
                for column in range(0, necessaryColumns):
                    # multiply elements at the same spot in frame and add it together
                    result = 0
                    for matrixRow in range(0, len(self.matrixes[0])):
                        for matrixCol in range(0, len(self.matrixes[0][0])):
                            for indepth in range(0, self.inputDepth):
                                result += self.matrixes[depth][matrixRow][matrixCol][indepth] * image[row * self.stride + matrixRow][column * self.stride + matrixCol][indepth]

                    newRow.append(result)
                newImage.append(newRow)
            newImages.append(newImage)

        #print(f"Conv Output: {newImage}")
        #print(f"Lenge Outputs: {len(newImage)}")
        return newImages

    def addPadding(self, image): # Veraltet und aktuell nicht funktionsfähig
        """
        Add padding with number 0 around the image with the width based on the matrix size

        Params:
            - image (2dim Array): Image to be padded

        Return:
            - newImage (2dim Array): Image with padding

        """
        return image
        #TODO: Support smaller padding
        paddingNumber = 0
        matLen = len(self.matrixes)
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

        ### Calculate  gradients to improve matrix ####

        kernalGradients = [[[[0 for _ in range(0, self.inputDepth)] for _ in self.matrixes[0][0]] for _ in self.matrixes[0]] for _ in self.matrixes]
        inputGradients = [[[0 for _ in range(0, self.inputDepth)] for _ in range(0, len(self.image[0]))] for _ in range(0, len(self.image))]

        #print(f"Kernal gradients: {kernalGradients}")
        #print(targets)
        #print(f"Lange Targets: {len(targets)}")
        #print(f"Lange Image: {len(self.image)}")

        for depth in range(0, len(targets)):

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
            
            for i in range(0, len(targets[depth])):
                row = []

                for j in range(0, len(targets[depth][0])):
                    row.append(targets[depth][i][j])
                    row += internalPadding

                if self.stride > 1:
                    row = row[:-(self.stride-1)]
                
                extendedGradient.append(row)
                
                zeroRow = []
                for j in range(0, len(row)):
                    zeroRow.append(0)

                for j in range(0, self.stride -1):
                    extendedGradient.append(zeroRow)

            if self.stride > 1:
                extendedGradient = extendedGradient[:-(self.stride-1)]

            # Calculate kernal gradients

            necessaryRows = int((len(self.image) - len(extendedGradient)) +1)
            necessaryColumns = int((len(self.image[0]) - len(extendedGradient[0])) +1)

            if necessaryRows != len(self.matrixes[depth]) or necessaryColumns != len(self.matrixes[depth][0]):
                raise Exception("There must be found frames for each part of the matrix")

            # Move targets over image
            for rowIndex in range(0, necessaryRows):
                for columnIndex in range(0, necessaryColumns):

                    val = [0 for _ in range(0, self.inputDepth)]
                    for targetRowIndex in range(0, len(extendedGradient)):
                        for targetColIndex in range(0, len(extendedGradient[0])):
                            for inDepth in range(0, self.inputDepth):
                                val[inDepth] += self.image[rowIndex + targetRowIndex][columnIndex + targetColIndex][inDepth] * extendedGradient[targetRowIndex][targetColIndex] #/ self.inputDepth # Might remove or adapt /self.inputDepth
                    kernalGradients[depth][rowIndex][columnIndex] = val
            
            #print(f"Kernal Gradients: {kernalGradients}")
            #print(f"Extended Gradients: {extendedGradient}")


            ### Calculate errors to propagate further ####

            # pad extended gradient with zeros around 
            paddedGradient = []

            firstline = []
            for i in range(0, len(extendedGradient[0]) + 2 * (len(self.matrixes[depth]) - 1)):
                firstline.append(0)
            #print(f"Lange First Line: {len(firstline)}")

            for i in range(0, len(self.matrixes[depth]) -1):
                paddedGradient.append(firstline)

            for i in range(0, len(extendedGradient)):
                line = []
                for j in range(0, len(self.matrixes[depth]) -1):
                    line.append(0)
                line += extendedGradient[i]
                for j in range(0, len(self.matrixes[depth]) -1):
                    line.append(0)
                paddedGradient.append(line)

            for i in range(0, len(self.matrixes[depth]) -1):
                paddedGradient.append(firstline)

            #print(f"Padded Gradients: {paddedGradient}")

            #print(f"Lange Extended Gradients: {len(extendedGradient)}")
            #print(f"Lange Padded Gradients: {len(paddedGradient)}")

            # Turn matrix around 180 degree
            turnedMatrix=[]
            for row in reversed(self.matrixes[depth]):
                newRow = []
                for col in reversed(row):
                    newRow.append(col)
                turnedMatrix.append(newRow)

            ### Calculate input errors

            necessaryRows = int((len(paddedGradient) - len(turnedMatrix)) + 1)
            necessaryColumns = int((len(paddedGradient[0]) - len(turnedMatrix[0])) + 1)

            if necessaryRows != len(self.image) or necessaryColumns != len(self.image[0]) or self.inputDepth != len(self.image[0][0]):
                raise Exception("There must be a gradient for each input")
            
            # Move matrix over extended gradients
            for rowIndex in range(0, necessaryRows):
                for columnIndex in range(0, necessaryColumns):
                    for targetRowIndex in range(0, len(turnedMatrix)):
                        for targetColIndex in range(0, len(turnedMatrix[0])):
                            for inDepth in range(0, self.inputDepth):
                                inputGradients[rowIndex][columnIndex][inDepth] += paddedGradient[rowIndex + targetRowIndex][columnIndex + targetColIndex] * turnedMatrix[targetRowIndex][targetColIndex][inDepth]
                    

        ### Adapt Gradients of matrix
        for depth in range(0, len(self.matrixes)):
            for rowIndex in range(0, len(self.matrixes[0])):
                for rowCol in range(0, len(self.matrixes[0][0])):
                    for inDepth in range(0, self.inputDepth):
                        self.matrixes[depth][rowIndex][rowCol][inDepth] -= learningRate * kernalGradients[depth][rowIndex][rowCol][inDepth]

        #print(len(inputGradients))      ### TODO: Length of input gradients should match input image ( - padding)

        ### Convert image gradients to 1dim array TODO: Anpassen für mehrdimensionale Werte
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
        return self.matrixes
    

    def getStructure(self):
        """
        Get structure of layer

        Returns:
        - 
        """
        return [LayerType.conv.value, [self.getWeights(), self.stride, self.padding.value]]
 