from layer.layer import Layer
from foundation.functions import Functions

class SequentialModel:

    def __init__(self, layers) -> None:
        self.layers = layers

        #Check if model is configured correct, so there are number of initial values as Perceptons of above layer + 1
        for index in range(1, len(layers)):
            bias = 1
            countOfIns = len(self.layers[index -1].perceptrons) + bias
            for i in range(0, len(self.layers[index].perceptrons)):
                if len(self.layers[index].perceptrons[i].weights) != countOfIns:
                    raise Exception("There must be initial values for above perceptons + 1")


    def act(self, values):

        # Append bias for input layer
        values_modified = values[:]
        values_modified.append(1)

        for index in range(0, len(self.layers)):
            values_modified = self.layers[index].act(values_modified)
        return values_modified
    
    def handleError(self, targets, errorFunc, learningRate):
        for index in range(0, len(self.layers)):
            # handle error from last to first layer
            targets = self.layers[len(self.layers) - index -1].handleError(targets, errorFunc, learningRate)

    def getWeights(self):
        weights = []
        for index in range(0, len(self.layers)):
            weights.append(self.layers[index].getWeights())
        return weights
