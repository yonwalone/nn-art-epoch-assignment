from foundation.functions import Functions

class PoolLayer:

    def __init__(self, function= Functions.max, poolSize = 2, stride=1, toList = False):
        self.poolSize = poolSize
        self.stride = stride
        self.function = function
        self.toList = toList

    def act(self, image):
        necessaryRows = int((len(image) - self.poolSize)/self.stride + 1)
        necessaryColumns = int((len(image[0]) - self.poolSize)/self.stride + 1)

        #print(image)
        #print(necessaryRows)
        #print(necessaryColumns)
        #print("Start Pooling")

        newImage=[]

        for row in range(0, necessaryRows):
            newRow = []
            for column in range(0, necessaryColumns):
                # Get value for field
                results = []
                for poolRow in range(0, self.poolSize):
                    for poolCol in range(0, self.poolSize):
                        results.append(image[row * self.stride + poolRow][column * self.stride + poolCol])
                
                #print(results)
                
                result = None
                if self.function == Functions.max:
                    result = max(results)

                if self.function == Functions.avg:
                    result = int(sum(results) / len(results))

                if result == None:
                    raise Exception("Use valid pooling function")

                newRow.append(result)
            newImage.append(newRow)

       # print(newImage)

        # Convert to 1dim list
        if self.toList:
            newList = []
            for index in range(0, len(newImage)):
                newList += newImage[index]
            newImage = newList
            #newImage = []
            #for index in range(0, len(newList)):
            #    newImage.append([newList[index]])
            #print(newImage)

        return newImage
    
    def handleError(self, targets, errorFunc, learningRate):
        return None
    
    def getWeights(self):
        return None
