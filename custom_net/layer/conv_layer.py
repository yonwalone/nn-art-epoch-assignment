

class CONVLayer:

    def __init__(self, matrix, stride = 1, padding = False):
        self.matrix = matrix
        self.stride = stride
        self.padding = padding

        self.matrix_height = len(self.matrix)
        
        self.matrix_width = len(self.matrix[0])
        for parameterIndex in range(0, self.matrix_height):
            if(len(self.matrix[parameterIndex]) != self.matrix_width):
                raise Exception("Matrix must has the same width in all rows")
            
    def act(self, image):
        # image is 3 dim array or 2dim ???
        image_height = len(image)
        image_width = len(image[0])
        #print(image)
        if self.padding:
            image = self.addPadding(image)
        #print(image)

        necessaryRows = int((len(image) - len(self.matrix))/self.stride + 1)
        necessaryColumns = int((len(image[0]) - len(self.matrix[0]))/self.stride + 1)
        
        newImage = []
        for row in range(0, necessaryRows):
            newRow = []
            for column in range(0, necessaryColumns):
                # Get value for field
                result = 0
                for matrixRow in range(0, len(self.matrix)):
                    for matrixCol in range(0, len(self.matrix[0])):
                        result += self.matrix[matrixRow][matrixCol] * image[row * self.stride + matrixRow][column * self.stride + matrixCol]

                newRow.append(result)
            newImage.append(newRow)

        #print(newImage)
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
        return None

    def getWeights(self):
        return None

    


    