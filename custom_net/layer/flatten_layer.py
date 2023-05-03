from foundation.enums import LayerType
from layer.layer_interface import LayerInterface

class FlattenLayer(LayerInterface):

    def __init__(self):
        """
        Initialize flatten layer.
        """
        pass

    def act(self, inputs):
        """
        Flatten image input to array.

        Params:
            - inputs: Image as input

        Returns:
            - newList: image data in array
        """
        #print(inputs)

        # Convert to 1dim list
        newList = self.flatInput(inputs)
        #print(f"After flat: {len(newList)}")

        # Append 1 as bias for next layer
        newList.append(1)

        #print(f"Flatten output: {newList}")
        return newList
    
    def flatInput(self,array):
        output= []

        for a in array:
            if isinstance(a, float) or isinstance(a, int):
                output.append(a)
            else:
                output += self.flatInput(a)
        return output


    def handleError(self, targets, errorFunc, learningRate):
        """
        Handle error for flatten layer and convert them into 1 dim Array.

        Params:
            -  targets: recieved error
            -  errorFunc: error function to initially calculate error
            -  learningRate (Float): Factor how strong weights are changed based on error

        Return:
            - derivateIn (1dim Array): error for next layer


        """
        # add incoming derivates together
        #print(f"Flatten Input Lenght: {len(targets)}")
        derivateIn = []
        for target in targets:
            value = 0
            for val in target:
                value += val
            derivateIn.append(value)
        return derivateIn

    
    def getStructure(self):
        """
        Get structure of layer

        Returns:
        - (Array): information about structure of layer
        """
        return [LayerType.flatten.value]