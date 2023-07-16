
class LayerInterface:

    # Process input and return response of layer
    def act(self, inputs):
        pass

    # Handle recieving targets, change weights and return errors for higher layer
    def handleError(self, targets, errorFunc, learningRate):
        pass

    # Return structure of layer
    def getStructure(self):
        pass