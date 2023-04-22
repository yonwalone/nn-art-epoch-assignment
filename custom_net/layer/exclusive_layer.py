from layer.layer_interface import LayerInterface
class FooLayer(LayerInterface):

    def __init__(self) -> None:
        pass

    def act(self, input):
        #print(input)

        #TODO: what if inputs are negative?
        self.input = input
        sum = 0
        for element in input:
            #print(element)
            sum += abs(element)

        self.sum = sum

        result = []
        for index in range(0, len(input)):
            result.append(input[index]/sum)

        with open("log.txt", 'a') as log_file:
            log_file.write(str(result) + "\n")

        return result
    
    def handleError(self, targets, errorFunc, learningRate):
        
        newTargets = []
        for target in targets:
            newTargets.append(target * self.sum)

        return newTargets



        

        