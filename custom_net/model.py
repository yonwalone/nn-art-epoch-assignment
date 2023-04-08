from layer.layer import Layer
from foundation.functions import Functions

class SequentialModel:

    def __init__(self, layers) -> None:
        self.layers = layers

    def act(self, values):
        for index in range(0, len(self.layers)):
            values = self.layers[index].act(values)
        return values
    
    def handleError(self, targets, errorFunc, learningRate):
        for index in range(0, len(self.layers)):
            # handle error from last to first layer
            targets = self.layers[len(self.layers) - index -1].handleError(targets, errorFunc, learningRate)

    def getWeights(self):
        weights = []
        for index in range(0, len(self.layers)):
            weights.append(self.layers[index].getWeights())
        return weights
