from layer.layer_interface import LayerInterface

class CONVLayer(LayerInterface):

    def __init__(self, matrix, stride = 1, padding = False):
        self.matrix = matrix
        self.stride = stride
        self.padding = padding

        # Check if matrix is square
        for parameterIndex in range(0, len(self.matrix)):
            if(len(self.matrix[parameterIndex]) != len(self.matrix[0])):
                raise Exception("Matrix must has the same width in all rows")
            
    def act(self, image):

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
        paddingNumber = len(self.matrix) -1 # Expect square

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
        print(self.image)
        print(targets)

        for row in range(0, len(targets)):
            for col in range(0, len(targets[0])):
                if targets[row][col] == 0:
                    continue

                for rowMat in range(0, len(self.matrix)):
                    for colMat in range(0, len(self.matrix[0])):
                        g = 9

        #TODO: Continue here

        return None

    def getWeights(self):
        pass
    

    def getStructure(self):
        pass
 