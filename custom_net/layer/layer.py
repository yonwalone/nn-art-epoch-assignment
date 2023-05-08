from foundation.enums import Functions, LayerType
from foundation.percepton import Percepton
from layer.layer_interface import LayerInterface

class Layer(LayerInterface):
    
    def __init__(self, count, function, initialWeights = None, isOutput = False):
        """
        Initialize layer with perceptons.

        Args:
            - count (int): Number of perceptons to be created in layer
            - function (Functions): activation functions for perceptons
            - initial Weights (2dim Array): Initial weights for inputs of perceptons
            - isOutput (Bool): Is output layer
        """
        self.isOutput = isOutput
        self.function = function

        # Create perceptrons of layer
        self.perceptrons = []
        if initialWeights != None:
            self.perceptrons = [Percepton(func=function, weights=initialWeights[index]) for index in range(count)]
        else:
            self.perceptrons = [Percepton(func=function, weights=None) for index in range(count)]

    def act(self, inputs):
        """
        Execute predictions for each perceptons with inputs and return responses

        Args:
            - inputs (Array): Input values for perceptons

        Return:
            - outputs (Array): outputs of each percepton
        """

        outputs = []
        # run each perceptron with input and add to list
        for perceptron in self.perceptrons:
            outputs.append(perceptron.act(inputs))
        
        # append bias
        if not self.isOutput:
            outputs.append(1)

        self.lastResults = outputs

        return outputs
    
    def handleError(self, targets, errorFunc, learningRate):
        """
        Handle error for layer, force perceptons to handle error and propagate error further

        Params:
            -  targets: recieved error / expected output at last layer
            -  errorFunc: error function to initially calculate error
            -  learningRate (Float): Factor how strong weights are changed based on error

        Return:
            - errorListSorted (2dim Array): errors clustered by input to which the errors should be propagated

        """

        if len(targets) != len(self.perceptrons):
            raise Exception("There must be targets for each Perceptons")
            
        errorList = []
        # Handle error for each perceptron
        for index, perceptron in enumerate(self.perceptrons):
            if self.isOutput:
                #targets is array
                errorList.append(perceptron.handleErrorOutput(targets[index], errorFunc, learningRate))
            else:
                #targets is 2dim array
                errorList.append(perceptron.handleError(targets[index], learningRate))

        # Sort errors for each input
        numberOfInputs = len(errorList[0])
        errorListSorted = []
        for index in range(0, numberOfInputs):
            errorsOfInput = []
            for error in errorList:
                errorsOfInput.append(error[index])
            errorListSorted.append(errorsOfInput)

        # Remove last element, because further optimization for bias is not possible
        errorListSorted.pop()

        return errorListSorted
    
    def getWeights(self):
        """
        Get weights of layer

        Returns:
        - weights (2dim Array): weights of each perceptons in layer
        """
        weights = []
        for perceptron in self.perceptrons:
            weights.append(perceptron.getWeights())
        return weights
    
    def getStructure(self):
        """
        Get structure of layer

        Returns:
        - (Array): information about structure of layer
        """
        return [LayerType.dense.value, [len(self.perceptrons), self.function.value, self.getWeights(), self.isOutput]]
