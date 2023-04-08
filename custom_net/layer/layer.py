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

        return outputs
