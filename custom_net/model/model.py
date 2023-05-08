from foundation.enums import Functions, TestTypes
from foundation.helper import print_progress_bar
from layer.layer import Layer

class SeqModel:

    def __init__(self, layers, onlyMLP = False) -> None:
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
            #print(values_modified)
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

    def train(self, input, output, errorFunc, learningRate, epochs):
        """
        Train model with inputs to return expected outputs.

        Params:
            - input: array of inputs of model
            - output: array of expected outputs of model
            - errorFunc: Error Function to calculate error
            - learningRate (Number): Factor of how fast a net should adapt to input values
            - epochs (Int): How many times should inputs be used
        """

        if len(input) != len(output):
            raise Exception("Len of inputs must equal the length of expected outputs")
        
        for epochIndex in range(0, epochs):

            for index, currOutput in enumerate(output):
                #print(f"Epoch: {epochIndex}, Input: {index}")
                print_progress_bar(index, len(output), start_text =f"Train: Epoch: {epochIndex}, Input", new_line = False)
                #print(f"Input: {input[indexOutput]}")
                #print(f"Expected Output: {output[indexOutput]}")
                self.act(input[index])
                self.handleError(targets=currOutput, errorFunc=errorFunc, learningRate=learningRate)       

        #print(f"Gewichte: {model.getWeights()}")

    def test(self, input, output, mode):
        """
        Test model with inputs and find percentage of correct outputs
        Params:
            - input: array of inputs of model
            - output: array of expected outputs of model
            - mode (TestTypes): how should be decided if result is correct

        Returns:
            - accuracy: percentage of correct found 
        """

        if mode == TestTypes.biggestPredictionOn1Position:
            errorCount= 0
            statistic = [[ 0 for _ in range(0,len(output[0]))] for _ in range(0,len(output[0]))]
            for ind in range(0, len(output)):
                #print(f"Test: {ind}")
                print_progress_bar(ind, len(output),start_text =f"Test", new_line = True)
                result = self.act(input[ind])
                print(result)

                # find 1 in output
                expIndex = output[ind].index(max(output[ind]))

                index = result.index(max(result))
                statistic[expIndex][index] += 1
                if output[ind][index] != 1:
                    errorCount += 1
            print(f"Error Count: {errorCount}")
            accuracy = 1 - errorCount / len(output)
            return accuracy, statistic

        else:
            raise Exception("Use implemented TestType")



