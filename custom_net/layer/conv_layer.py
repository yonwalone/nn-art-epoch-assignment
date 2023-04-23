from foundation.enums import PaddingType
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
        #print("Handle")
        # evaluate how often the matrix is moved down and moved right per row
        necessaryRows = int((len(self.image) - len(self.matrix))/self.stride + 1)
        necessaryColumns = int((len(self.image[0]) - len(self.matrix[0]))/self.stride + 1)

        if (necessaryRows * necessaryColumns != len(targets) * len(targets[0])):
            raise Exception("Number of targets must match number of patches")
        
        #print(self.matrix)

        for rowIndex in range(0, necessaryRows):
            for columnIndex in range(0, necessaryColumns):
                if targets[rowIndex][columnIndex] == 0:
                    continue

                # For all patches  
                for matrixRowIndex in range(0, len(self.matrix)):
                    for matrixColIndex in range(0, len(self.matrix[0])):
                        self.matrix[matrixRowIndex][matrixColIndex] += (
                            learningRate * 
                            self.matrix[matrixRowIndex][matrixColIndex] * 
                            targets[rowIndex][columnIndex] * 
                            self.image[rowIndex * self.stride + matrixRowIndex][columnIndex * self.stride + matrixColIndex]
                        )

                
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
 