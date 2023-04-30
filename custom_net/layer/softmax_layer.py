from layer.layer_interface import LayerInterface
from foundation.enums import LayerType

class SoftMaxLayer(LayerInterface):

    def __init__(self) -> None:
        """
        Initialize softmax layer.
        """
        pass

    def act(self, inputs):
        """
        Normalize outputs to 100%

        Params:
            - inputs: output values

        Returns:
            - newList: normalized outputs
        """

        #TODO: what if inputs are negative?
        self.inputs = inputs
        #print(f"Act Dense Output: {self.inputs}")
        self.sum = sum(abs(e) for e in inputs)

        if self.sum == 0:
            return self.inputs

        result = []
        for input in inputs:
            result.append(input/self.sum)

        return result
    
    def handleError(self, targets, errorFunc, learningRate):
        """
        Convert targets to match the recent sum

        Params:
            -  targets: expected output
            -  errorFunc: error function to initially calculate error
            -  learningRate (Float): Factor how strong weights are changed based on error

        Return:
            - newTargets (1dim Array): targets for layer before

        """
        #if self.sum == 0: # Might remove
            #self.sum = 1
        
        newTargets = []
        for target in targets:
            newTargets.append(target * self.sum)

        #print(f"Softmax Targets: {newTargets}")

        return newTargets

    def getStructure(self):
        """
        Get structure of layer

        Returns:
        - (Array): information about structure of layer
        """
        return [LayerType.softmax.value]

        

        