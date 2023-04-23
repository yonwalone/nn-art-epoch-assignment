from layer.layer import Layer
from foundation.enums import Functions

class SeqModel:

    def __init__(self, layers, onlyMLP = True) -> None:
        """
        Initialize model with layers.

        Args:
            - layers (LayerInterace): Layers to be added in order to model from top to buttom
            - onlyMLP (Bool): does model only include fully connected layer
        """

        self.layers = layers
        self.onlyMLP = onlyMLP

        return
    
        #TODO: Must be adapted for convolutional and pooling layer

        #Check if model is configured correct, so there are number of initial values as Perceptons of above layer + 1
        for index in range(1, len(layers)):
            bias = 1
            countOfIns = len(self.layers[index -1].perceptrons) + bias
            for i in range(0, len(self.layers[index].perceptrons)):
                if len(self.layers[index].perceptrons[i].weights) != countOfIns:
                    raise Exception("There must be initial values for above perceptons + 1")


    def act(self, values):
        """
        Predict for values by putting them in first layer and than the results into the next and return end result

        Args:
            - values (Array): Input values for model

        Return:
            - valuesModified (Array): outputs of model
        """

        # Append bias for input layer
        values_modified = values[:]
        if self.onlyMLP:
            values_modified.append(1)

        # Provide input for each layer, process input, provide result as next input
        for layer in self.layers:
            values_modified = layer.act(values_modified)
        return values_modified
    
    def handleError(self, targets, errorFunc, learningRate):
        """
        Handle expected targets for model, put errors from last to first layer

        Params:
            -  targets: expected output of model
            -  errorFunc: error function to initially calculate error
            -  learningRate (Float): Factor how strong weights are changed based on error
        """
        for layer in reversed(self.layers):
            # handle error from last to first layer
            targets = layer.handleError(targets, errorFunc, learningRate)

    def getWeights(self):
        """
        Get weights of perceptons in layers

        Returns:
        - weights (3dim Array): weights of each perceptons in layers
        """
        weights = []
        for layer in self.layers:
            weights.append(layer.getWeights())
        return weights
    
    def getStructure(self):
        """
        Get structure of model

        Returns:
        - structure (2dim Array): information about structure of model
        """
        structure = []
        for layer in self.layers:
            structure.append(layer.getStructure())
        return structure
