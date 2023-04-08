from foundation.neuron import Percepton
from foundation.functions import Functions

class Layer:
    
    def __init__(self, count, function, initialWeights, biasValue = 1, isOutput = False):
        self.isOutput = isOutput
        self.biasValue = biasValue

        self.perceptrons = []
        for index in range(0, count):
            #print("Create Perceptron")
            self.perceptrons.append(Percepton(func=function, weights=initialWeights[index]))

    def act(self, inputs):

        outputs = []
        for index in range (0, len(self.perceptrons)):
            outputs.append(self.perceptrons[index].react(inputs))

        if not self.isOutput:
            outputs.append(self.biasValue)

        self.lastResults = outputs

        return outputs
    
    def handleError(self,targets, errorFunc, learningRate):
        #targets is list
        
        if self.isOutput:
            if len(targets) != len(self.perceptrons):
                raise Exception("There must be targets for each Perceptons")
            
            #2dim list:
            errorList = []
            for index in range(0, len(self.perceptrons)):
                errorList.append(self.perceptrons[index].handleErrorOutput(targets[index], errorFunc, learningRate))

            #print(errorList)

            #Sort errors for each input
            numberOfInputs = len(errorList[0])
            errorListSorted = []
            for index in range(0, numberOfInputs):
                errorsOfInput = []
                for i in range(0,len(errorList)):
                    errorsOfInput.append(errorList[i][index])
                errorListSorted.append(errorsOfInput)
            
            #print(errorListSorted)

            return errorListSorted # oder vl. hier schon für die nächste Ebene verarbeiten

    
    def getLastResults(self):
        return self.lastResults
