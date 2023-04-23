from layer.layer_interface import LayerInterface
class FooLayer(LayerInterface):

    def __init__(self) -> None:
        pass

    def act(self, input):
        #print(input)

        with open("log.txt", 'a') as log_file:
            log_file.write(str(input) + "\n")

        #TODO: what if inputs are negative?
        self.input = input
        sum = 0
        for element in input:
            #print(element)
            sum += abs(element)

        self.sum = sum

        result = []
        if sum != 0:
            for index in range(0, len(input)):
                result.append(input[index]/sum)
        else:
            for index in range(0, len(input)):
                result.append(input[index])


        with open("log.txt", 'a') as log_file:
            log_file.write(str(result) + "\n")

        return result
    
    def handleError(self, targets, errorFunc, learningRate):
        
        newTargets = []
        for target in targets:
            newTargets.append(target * self.sum)

        with open("log.txt", 'a') as log_file:
            log_file.write(str(newTargets) + "\n")

        return newTargets



        

        