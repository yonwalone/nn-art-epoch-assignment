from layer.layer_interface import LayerInterface

class SoftMaxLayer(LayerInterface):

    def __init__(self) -> None:
        pass

    def act(self, inputs):
        #print(input)

        #TODO: what if inputs are negative?
        self.inputs = inputs
        self.sum = sum(abs(e) for e in inputs)

        result = []
        for input in inputs:
            result.append(input/self.sum)

        return result
    
    def handleError(self, targets, errorFunc, learningRate):
        
        newTargets = []
        for target in targets:
            newTargets.append(target * self.sum)

        return newTargets



        

        