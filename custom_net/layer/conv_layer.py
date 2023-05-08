import random as rnd

from foundation.enums import PaddingType, LayerType
from foundation.helper import flatInput
from layer.layer_interface import LayerInterface

class CONVLayer(LayerInterface):

    def __init__(self, matrix = 3, stride = 1, inputDepth = 1, depth = 1, bias = None, padding = PaddingType.valid):
        """
        Initialize convolutional layer.

        Args:
            - matrix (4dim Array): Matrix to use in transformation [depth [inputDepth [height [width]]]]
            - stride (Int): Distance to move matrix over image
            - padding (Bool): Should padding be added to image
        """

        if type(matrix) == int:
            self.matrixes = []
            for d in range(0, depth):
                row = []
                for inp in range(0, inputDepth):
                    spot = []
                    for index in range(0, matrix):
                        place = []
                        for i in range(0, matrix):
                            place.append(rnd.random())
                        spot.append(place)
                    row.append(spot)
                self.matrixes.append(row)       

        else:
            self.matrixes = matrix

        self.stride = stride
        self.paddingType = padding
        self.inputDepth = inputDepth
        self.depth = depth
        self.bias = bias

        # Check if matrix is allowed
        if any(len(row) != len(self.matrixes[0]) for row in self.matrixes):
            raise Exception("Matrix must have the same width in all rows")

            
    def act(self, image):
        """
        Transform image based on the settings of the layer.

        Args:
            - image (3dim Array): Image to put into layer, [inputdepth [height [width]]]

        Return:
            - newImage: Transformed image 
        """

        #print(f"Len Input: {len(image)}")

        # Add padding around image
        image = self.addPadding(image)
            
        self.image = image 

        if (len(image[0]) - len(self.matrixes[0][0]))/self.stride % 1 != 0.0 or (len(image[0][0]) - len(self.matrixes[0][0][0]))/self.stride % 1  != 0:
            raise Exception(f"Size of matrix, stride and image does not fit together, change matrix or stride")

        # evaluate how often the matrix is moved down and moved right per row
        necessaryRows = int((len(image[0]) - len(self.matrixes[0][0]))/self.stride + 1)
        necessaryColumns = int((len(image[0][0]) - len(self.matrixes[0][0][0]))/self.stride + 1)

        if self.bias == None:
            self.bias = []                          # [depth [height [width]]]
            for depth in range(0, self.depth):
                matrix = []
                for row in range(0, necessaryRows):
                    newRow = []
                    for col in range(0, necessaryColumns):
                        newRow.append(rnd.random())
                    matrix.append(newRow)             
                self.bias.append(matrix)
        
        # move matrix over image
        newImages = []
        for depth in range(0, self.depth):
            newImage = []
            for row in range(0, necessaryRows):
                newRow = []
                for column in range(0, necessaryColumns):
                    # multiply elements at the same spot in frame and add it together
                    result = 0
                    for matrixRow in range(0, len(self.matrixes[0][0])):
                        for matrixCol in range(0, len(self.matrixes[0][0][0])):
                            for indepth in range(0, self.inputDepth):
                                result += (self.matrixes[depth][indepth][matrixRow][matrixCol] * image[indepth][row * self.stride + matrixRow][column * self.stride + matrixCol] + self.bias[depth][matrixRow][matrixCol]) / (len(self.matrixes[0][0])*len(self.matrixes[0][0][0])) # Might remove division

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

        self.paddingSize = 0
        matLen = len(self.matrixes[0][0])
        if self.paddingType == PaddingType.same:
            self.paddingSize = (matLen - (matLen % 2)) //2
        if self.paddingType == PaddingType.full:
            self.paddingSize = matLen - 1

        #print(self.paddingSize)
       
        newImages=[]
        for inDepth in range(0, self.inputDepth):
            newImage = []
            # Padding lines
            paddingLine = [0] * (self.paddingSize + len(image[inDepth]) + self.paddingSize)

            # Append start padding
            newImage.extend([paddingLine] * self.paddingSize)

            # Add padding to beginning and end of each row
            for row in image[inDepth]:
                padded_row = [0] * self.paddingSize + row + [0] * self.paddingSize
                newImage.append(padded_row)

            # Append end padding
            newImage.extend([paddingLine] * self.paddingSize)
            newImages.append(newImage)

        #print(f"Image: {image}")
        #print(f"Padded Image: {newImages}")

        return newImages


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

        kernalGradients = [[[[0 for _ in self.matrixes[0][0][0]] for _ in self.matrixes[0][0]] for _ in self.matrixes[0]] for _ in self.matrixes]
        inputGradients = [[[0 for _ in range(0, len(self.image[0][0]))] for _ in range(0, len(self.image[0]))] for _ in range(0, self.inputDepth)]

        # For each depth in targets
        for depth in range(0, len(targets)):

            # Anti normalize targets TODO: Might remove 
            for row in range(0, len(targets[depth])):
                for col in range(0, len(targets[depth][0])):
                    targets[depth][row][col] *= (len(self.matrixes[0][0])*len(self.matrixes[0][0][0]))


            #print(self.bias)
            ### Adapt values for bias
            for row in range(0, len(targets[depth])):
                for col in range(0, len(targets[depth][0])):
                    self.bias[depth][row][col] -= learningRate * targets[depth][row][col] / self.inputDepth # TODO: Might remove devision
            #print("Second")
            #print(self.bias)
            

            ### Prepare Gradient: Add zeros between targets based on stride

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


            ### Calculate kernal gradients

            necessaryRows = int((len(self.image[0]) - len(extendedGradient)) +1)
            necessaryColumns = int((len(self.image[0][0]) - len(extendedGradient[0])) +1)

            if necessaryRows != len(self.matrixes[depth][0]) or necessaryColumns != len(self.matrixes[depth][0][0]):
                raise Exception("There must be found frames for each part of the matrix")

            # Move targets over image
            for rowIndex in range(0, necessaryRows):
                for columnIndex in range(0, necessaryColumns):

                    for targetRowIndex in range(0, len(extendedGradient)):
                        for targetColIndex in range(0, len(extendedGradient[0])):
                            for inDepth in range(0, self.inputDepth):
                                kernalGradients[depth][inDepth][rowIndex][columnIndex] += self.image[inDepth][rowIndex + targetRowIndex][columnIndex + targetColIndex] * extendedGradient[targetRowIndex][targetColIndex] #/ self.inputDepth # Might remove or adapt /self.inputDepth
            
            #print(f"Kernal Gradients: {kernalGradients}")
            #print(f"Extended Gradients: {extendedGradient}")


            ### Calculate input errors to propagate further ####

            # pad extended gradient with zeros around 
            paddedGradient = []

            firstline = []
            for i in range(0, len(extendedGradient[0]) + 2 * (len(self.matrixes[depth][0]) - 1)):
                firstline.append(0)

            for i in range(0, len(self.matrixes[depth][0]) -1):
                paddedGradient.append(firstline)

            for i in range(0, len(extendedGradient)):
                line = []
                for j in range(0, len(self.matrixes[depth][0]) -1):
                    line.append(0)
                line += extendedGradient[i]
                for j in range(0, len(self.matrixes[depth][0]) -1):
                    line.append(0)
                paddedGradient.append(line)

            for i in range(0, len(self.matrixes[depth][0]) -1):
                paddedGradient.append(firstline)

            #print(f"Padded Gradients: {paddedGradient}")     

            # Turn matrix around 180 degree
            turnedMatrixes=[]                           # [indepth [height [width]]]
            for indepth in range(0, len(self.matrixes[depth])):
                turnedMatrix = []
                for row in reversed(self.matrixes[depth][indepth]):
                    newRow = []
                    for col in reversed(row):
                        newRow.append(col)
                    turnedMatrix.append(newRow)
                turnedMatrixes.append(turnedMatrix)


            necessaryRows = int((len(paddedGradient) - len(turnedMatrixes[0])) + 1)
            necessaryColumns = int((len(paddedGradient[0]) - len(turnedMatrixes[0][0])) + 1)

            if necessaryRows != len(self.image[0]) or necessaryColumns != len(self.image[0][0]) or self.inputDepth != len(self.image):
                raise Exception("There must be a gradient for each input")
            
            # Move matrix over extended gradients
            for rowIndex in range(0, necessaryRows):
                for columnIndex in range(0, necessaryColumns):
                    for targetRowIndex in range(0, len(turnedMatrixes[0])):
                        for targetColIndex in range(0, len(turnedMatrixes[0][0])):
                            for inDepth in range(0, self.inputDepth):
                                inputGradients[inDepth][rowIndex][columnIndex] += paddedGradient[rowIndex + targetRowIndex][columnIndex + targetColIndex] * turnedMatrixes[inDepth][targetRowIndex][targetColIndex]       

        ### Adapt Gradients of matrix
        for depth in range(0, len(self.matrixes)):
            for rowIndex in range(0, len(self.matrixes[0][0])):
                for rowCol in range(0, len(self.matrixes[0][0][0])):
                    for inDepth in range(0, self.inputDepth):
                        self.matrixes[depth][inDepth][rowIndex][rowCol] -= learningRate * kernalGradients[depth][inDepth][rowIndex][rowCol]

        ### Remove padding in inputGradients
        shrinkInputGradients = []
        for inDepth in range(0, len(inputGradients)):
            inputMatrix = []
            for row in range(0, len(inputGradients[inDepth])):
                if row < self.paddingSize:
                    continue
                if row >=  (len(inputGradients[inDepth]) - self.paddingSize):
                    continue
                newRow = []
                for col in range(0, len(inputGradients[inDepth][row])):
                    if col < self.paddingSize:
                        continue
                    if col >=  (len(inputGradients[inDepth][row]) - self.paddingSize):
                        continue
                    newRow.append(inputGradients[inDepth][row][col])
                inputMatrix.append(newRow)
            shrinkInputGradients.append(inputMatrix)

        ### Convert image gradients to 1dim array
        errors = flatInput(shrinkInputGradients)

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
        return [LayerType.conv.value, [self.getWeights(), self.stride, self.paddingType.value, self.inputDepth, self.depth, self.bias]]
 