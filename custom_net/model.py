from layer.layer import Layer
from foundation.functions import Functions

class SequentialModel:

    def __init__(self, layers) -> None:
        self.layers = layers

    def act(self, values):
        for index in range(0, len(self.layers)):
            values = self.layers[index].act(values)
        return values
    
    def handleError(error, function):
        if function == Functions.halfsquareError:
            b = 9
