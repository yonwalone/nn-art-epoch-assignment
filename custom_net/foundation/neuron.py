from foundation.functions import Functions

class Percepton:

    def __init__(self, func, weights) -> None:
        self.func = func
        self.weights = weights
        return
    
    def react(self, inputs):
        if len(self.weights) != len(inputs):
            raise Exception("Length of weights must be equal to length of inputs")
        
        sum = 0
        for index in range(0, len(self.weights)):
            #print("Added value")
            sum += inputs[index] * self.weights[index]

        if self.func == Functions.heaviside:
            if sum < 0:
                return 0
            else:
                return 1
    
        if self.func == Functions.sgn:
            if sum < 0:
                return -1
            if sum == 0:
                return 0
            return 1
        


