from layer.layer_interface import LayerInterface
class FooLayer(LayerInterface):

    def __init__(self) -> None:
        pass

    def act(self, inputs):
        #print(input)

        #TODO: what if inputs are negative?
        self.inputs = inputs
        self.sum = sum(abs(e) for e in inputs)

        result = []
        for input in inputs:
            result.append(input/sum)

        with open("log.txt", 'a') as log_file:
            log_file.write(str(result) + "\n")

        return result
    
    def handleError(self, targets, errorFunc, learningRate):
        
        newTargets = []
        for target in targets:
            newTargets.append(target * self.sum)

        return newTargets



        

        