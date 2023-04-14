from foundation.neuron import Percepton
from foundation.functions import Functions
from layer.layer_interface import LayerInterface

class Layer(LayerInterface):
    
    def __init__(self, count, function, initialWeights, isOutput = False):
        self.isOutput = isOutput
        self.function = function

        if count != len(initialWeights):
            raise Exception("There must be initialWeights for each Percepton")

        # Create perceptrons of layer
        self.perceptrons = []
        for index in range(0, count):
            self.perceptrons.append(Percepton(func=function, weights=initialWeights[index]))

    def act(self, inputs):

        outputs = []
        # run each perceptron with input and add to list
        for index in range (0, len(self.perceptrons)):
            outputs.append(self.perceptrons[index].react(inputs))
        
        # append bias
        if not self.isOutput:
            outputs.append(1)

        self.lastResults = outputs

        return outputs
    
    def handleError(self, targets, errorFunc, learningRate):

        if len(targets) != len(self.perceptrons):
            raise Exception("There must be targets for each Perceptons")
            
        errorList = []
        # Handle error for each perceptron
        for index in range(0, len(self.perceptrons)):
            if self.isOutput:
                #targets is array
                errorList.append(self.perceptrons[index].handleErrorOutput(targets[index], errorFunc, learningRate))
            else:
                #targets is 2dim array
                errorList.append(self.perceptrons[index].handleError(targets[index], learningRate))

        # Sort errors for each input
        numberOfInputs = len(errorList[0])
        errorListSorted = []
        for index in range(0, numberOfInputs):
            errorsOfInput = []
            for i in range(0,len(errorList)):
                errorsOfInput.append(errorList[i][index])
            errorListSorted.append(errorsOfInput)

        # Remove last element, because further optimization for bias is not possible
        errorListSorted.pop()

        return errorListSorted
    
    def getWeights(self):
        weights = []
        for index in range(0, len(self.perceptrons)):
            weights.append(self.perceptrons[index].getWeights())
        return weights
    
    def getLastResults(self):
        return self.lastResults
    
    def getStructure(self):
        return [len(self.perceptrons), self.function.value, self.isOutput]
